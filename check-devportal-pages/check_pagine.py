"""
Controllo delle pagine API di developer.pagopa.it

Ogni pagina mostra una specifica OpenAPI (file JSON) tramite il componente <rapi-doc>.
Lo script verifica che, dopo le modifiche ai file delle specifiche, le pagine
continuino a funzionare.

Per ogni link presente in links.txt:
  0. Cerca il menu a tendina delle versioni:
       - se non c'e', la pagina viene controllata una volta sola
       - se c'e', la pagina viene controllata una volta per ogni versione del menu
  Per ogni pagina (o versione):
  1. MAPPATURA: legge il titolo della pagina e l'attributo 'spec-url' di <rapi-doc>
     (link al file JSON della specifica).
  2. CONTROLLO FILE: chiama l'URL di spec-url. E' KO se risponde 400, 404 o 429
     (file inesistente o non raggiungibile), altrimenti e' OK.
  3. CONTROLLO PARSING: (solo se il controllo 2 e' OK) verifica che <rapi-doc>
     abbia renderizzato l'elemento con i due bottoni. Se manca, il parser
     di rapi-doc ha probabilmente avuto problemi con il contenuto del file.

Output: tabella a console + CSV nella cartella 'output/'.
Su GitHub Actions la tabella viene scritta anche nel riepilogo (Summary) dell'esecuzione.
Codice di uscita: 0 se tutti i controlli sono OK, 1 se almeno uno e' KO
(utile per l'esecuzione automatica, es. GitHub Actions).

Uso:  python check_pagine.py
"""

import csv
import os
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchShadowRootException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ----------------------------------------------------------------------------
# CONFIGURAZIONE
# ----------------------------------------------------------------------------

# Cartella dello script: i percorsi sotto sono relativi ad essa, quindi lo script
# funziona da qualunque cartella venga lanciato
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File con l'elenco dei link (uno per riga; righe vuote e righe con # vengono ignorate)
LINKS_FILE = os.path.join(BASE_DIR, "links.txt")

# Cartella in cui viene salvato il CSV dei risultati
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# True = Chrome senza finestra; False = il browser si apre e puoi vedere cosa succede
HEADLESS = True

# True = stampa a console il dettaglio dei passaggi per ogni pagina
DEBUG = True

# Attese massime (secondi)
PAGE_TIMEOUT = 20      # caricamento della pagina e comparsa di <rapi-doc>
PARSING_TIMEOUT = 15   # comparsa dei bottoni dentro <rapi-doc>
HTTP_TIMEOUT = 15      # chiamata HTTP al file spec-url
DROPDOWN_TIMEOUT = 3   # ricerca del menu delle versioni
OPTIONS_TIMEOUT = 4    # comparsa delle voci dopo l'apertura del menu
SWITCH_TIMEOUT = 5     # cambio di spec-url dopo la selezione di una versione

# Codici HTTP per cui il file della specifica e' considerato non valido
HTTP_KO_CODES = {400, 404, 429}

# Elemento che mostra la specifica (web component)
RAPIDOC_SELECTOR = "rapi-doc"

# Bottoni cercati DENTRO lo shadow DOM di <rapi-doc>.
# Selenium non permette XPath nello shadow DOM, quindi il percorso e' scritto in CSS
# (equivale a .../section/div[2]/div/button).
BUTTONS_CSS = "main > div > div > div > section > div:nth-child(2) > div > button"
EXPECTED_BUTTONS = 2

# Menu a tendina delle versioni (si trova nel DOM normale, quindi si usa XPath)
VERSION_DROPDOWN_XPATH = "/html/body/main/div/div/div[2]/div/div[1]/div/div/div"

# Voci del menu una volta aperto. I locator sono provati in ordine e si usa il primo
# che trova almeno una voce; vengono prese tutte le voci <li>, quindi funziona con
# qualsiasi numero di versioni.
OPTION_LOCATORS = [
    # percorso noto delle voci
    (By.XPATH, "/html/body/div[5]/div[3]/ul/li"),
    # alternativa se l'indice div[5] cambia: qualunque popup aperto che contiene una lista
    (By.XPATH, "/html/body/div[@role='presentation']//ul/li"),
    # alternativa basata sui ruoli ARIA
    (By.CSS_SELECTOR, "ul[role='listbox'] > li, ul[role='menu'] > li"),
]

# Valori della tabella finale
OK = "OK"
KO = "KO"
SKIPPED = "NON ESEGUITO"


# ----------------------------------------------------------------------------
# FUNZIONI DI SUPPORTO
# ----------------------------------------------------------------------------

def debug(message):
    """Stampa un messaggio solo se DEBUG e' attivo."""
    if DEBUG:
        print(f"    {message}")


def read_links(path):
    """Legge i link dal file di testo, ignorando righe vuote e commenti (#)."""
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line and not line.startswith("#")]


def create_driver():
    """Crea il browser Chrome controllato da Selenium."""
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--no-sandbox")             # necessario in molti ambienti CI
    options.add_argument("--disable-dev-shm-usage")  # evita crash per poca memoria condivisa
    options.add_argument("--log-level=3")            # meno rumore nel terminale
    # Selenium scarica da solo il driver adatto alla versione di Chrome installata
    return webdriver.Chrome(options=options)


def new_result(link, version):
    """Crea una riga di risultato con tutti i controlli 'NON ESEGUITO'."""
    return {
        "link": link,
        "versione": version,
        "titolo": "",
        "spec_url": "",
        "file_json": "",
        "controllo_pagina": SKIPPED,
        "dettaglio_pagina": "",
        "controllo_parsing": SKIPPED,
        "dettaglio_parsing": "",
        "note": "",
    }


def get_rapidoc(driver):
    """Ritorna l'elemento <rapi-doc> corrente (va ri-cercato dopo ogni cambio versione)."""
    return driver.find_element(By.CSS_SELECTOR, RAPIDOC_SELECTOR)


def get_page_title(driver):
    """Titolo della pagina: usa l'<h1> se presente, altrimenti il <title> del browser."""
    try:
        h1 = driver.find_element(By.TAG_NAME, "h1").text.strip()
        if h1:
            return h1
    except NoSuchElementException:
        pass
    return driver.title.strip()


def click_element(driver, element):
    """Click normale; se qualcosa lo intercetta, ripiega su un click via JavaScript."""
    try:
        element.click()
    except WebDriverException:
        driver.execute_script("arguments[0].click();", element)


# ----------------------------------------------------------------------------
# MENU DELLE VERSIONI
# ----------------------------------------------------------------------------

def find_version_dropdown(driver):
    """Cerca il menu delle versioni. Ritorna l'elemento oppure None se non esiste."""
    try:
        return WebDriverWait(driver, DROPDOWN_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, VERSION_DROPDOWN_XPATH))
        )
    except TimeoutException:
        return None


def find_options(driver):
    """
    Ritorna tutte le voci del menu aperto (lista vuota se il menu e' chiuso).
    Non si filtra per "visibilita'": durante l'animazione di apertura Selenium
    potrebbe considerare le voci invisibili anche se sono presenti.
    """
    for by, locator in OPTION_LOCATORS:
        options = driver.find_elements(by, locator)
        if options:
            return options
    return []


def debug_locators(driver):
    """Diagnostica: quante voci trova ciascun locator (aiuta ad aggiornare OPTION_LOCATORS)."""
    for by, locator in OPTION_LOCATORS:
        try:
            found = len(driver.find_elements(by, locator))
        except WebDriverException:
            found = "locator non valido"
        debug(f"  [diagnostica] {locator} -> {found} voci")


def open_menu(driver, dropdown):
    """
    Apre il menu e ritorna le sue voci.
    Sul sito il click non apre il menu, mentre il tasto INVIO si': e' il primo
    tentativo; il click resta come alternativa.
    """
    attempts = [
        ("tasto INVIO", lambda: dropdown.send_keys(Keys.ENTER)),
        ("click", lambda: click_element(driver, dropdown)),
    ]
    for name, attempt in attempts:
        try:
            attempt()
            WebDriverWait(driver, OPTIONS_TIMEOUT).until(lambda d: len(find_options(d)) > 0)
            options = find_options(driver)
            debug(f"  (menu aperto con {name}: {len(options)} voci)")
            return options
        except (TimeoutException, WebDriverException):
            continue  # provo il metodo successivo
    debug_locators(driver)
    raise TimeoutException("menu versioni non apribile o voci non trovate")


def close_menu(driver):
    """Chiude il menu aperto (tasto ESC) e attende che le voci spariscano."""
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    try:
        WebDriverWait(driver, 5).until(lambda d: len(find_options(d)) == 0)
    except TimeoutException:
        pass  # se resta aperto, il tentativo successivo lo gestisce


def list_versions(driver, dropdown):
    """Apre il menu, legge il nome di tutte le versioni e lo richiude."""
    options = open_menu(driver, dropdown)
    # textContent funziona anche se la voce non e' ancora "visibile" per Selenium
    labels = [
        (o.text or o.get_attribute("textContent") or "").strip() or f"versione {i}"
        for i, o in enumerate(options, start=1)
    ]
    close_menu(driver)
    return labels


def select_version(driver, index):
    """Seleziona nel menu la versione numero 'index' (0 = prima voce)."""
    dropdown = find_version_dropdown(driver)  # ri-cerco: la pagina puo' ridisegnarsi
    if dropdown is None:
        raise NoSuchElementException("menu versioni non piu' presente")
    options = open_menu(driver, dropdown)
    if index >= len(options):
        raise NoSuchElementException(f"voce {index} non trovata ({len(options)} voci)")
    click_element(driver, options[index])
    try:  # attendo che il menu si chiuda
        WebDriverWait(driver, 5).until(lambda d: len(find_options(d)) == 0)
    except TimeoutException:
        close_menu(driver)


def get_current_version_label(driver):
    """Testo mostrato dal menu, cioe' la versione attualmente attiva ('' se non leggibile)."""
    try:
        dropdown = find_version_dropdown(driver)
        return dropdown.text.strip() if dropdown is not None else ""
    except WebDriverException:
        return ""


def wait_spec_url_change(driver, previous):
    """Dopo la selezione di una versione, attende che spec-url cambi. True se e' cambiato."""
    try:
        WebDriverWait(
            driver, SWITCH_TIMEOUT,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        ).until(
            lambda d: get_rapidoc(d).get_attribute("spec-url") not in (None, "", previous)
        )
        return True
    except TimeoutException:
        return False


# ----------------------------------------------------------------------------
# CONTROLLI
# ----------------------------------------------------------------------------

def check_spec_file(spec_url):
    """
    Controllo file: il file indicato in spec-url esiste ancora?
    Ritorna (esito, dettaglio), es. ("OK", "HTTP 200") oppure ("KO", "HTTP 404").
    """
    try:
        # allow_redirects=False: un eventuale 302 resta visibile come tale
        # stream=True: non scarica il file, serve solo lo status
        response = requests.get(
            spec_url, allow_redirects=False, stream=True, timeout=HTTP_TIMEOUT
        )
        status = response.status_code
        response.close()
    except requests.RequestException as exc:
        return KO, f"errore di rete: {type(exc).__name__}"

    if status in HTTP_KO_CODES:
        return KO, f"HTTP {status}"
    return OK, f"HTTP {status}"


def count_buttons(rapidoc_element):
    """Conta i bottoni attesi dentro lo shadow DOM di <rapi-doc> (0 se non e' ancora pronto)."""
    try:
        shadow = rapidoc_element.shadow_root
        return len(shadow.find_elements(By.CSS_SELECTOR, BUTTONS_CSS))
    except (NoSuchShadowRootException, StaleElementReferenceException, WebDriverException):
        return 0


def check_parsing(driver):
    """
    Controllo parsing: <rapi-doc> ha renderizzato l'elemento con i due bottoni?
    Attende fino a PARSING_TIMEOUT secondi, perche' il rendering puo' essere lento.
    """
    def buttons_found(d):
        return count_buttons(get_rapidoc(d))

    try:
        WebDriverWait(
            driver, PARSING_TIMEOUT,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        ).until(lambda d: buttons_found(d) >= EXPECTED_BUTTONS)
        return OK, f"{EXPECTED_BUTTONS} bottoni trovati"
    except TimeoutException:
        try:
            found = buttons_found(driver)
        except WebDriverException:
            found = 0
        return KO, f"bottoni trovati: {found}/{EXPECTED_BUTTONS}"


def analyze_current_version(driver, link, version):
    """Esegue mappatura e controlli sulla versione attualmente mostrata nella pagina."""
    result = new_result(link, version)

    # --- STEP 1: mappatura titolo -> spec-url ---------------------------------
    debug("STEP 1 - Mappatura titolo -> spec-url")
    try:
        rapidoc = WebDriverWait(driver, PAGE_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, RAPIDOC_SELECTOR))
        )
        result["titolo"] = get_page_title(driver)
        spec_url = rapidoc.get_attribute("spec-url")
    except (TimeoutException, StaleElementReferenceException):
        result["controllo_pagina"] = KO
        result["dettaglio_pagina"] = "elemento <rapi-doc> non trovato nella pagina"
        debug(f"  -> KO: {result['dettaglio_pagina']}")
        debug("STEP 2 - Controllo file: NON ESEGUITO")
        debug("STEP 3 - Controllo parsing: NON ESEGUITO")
        return result

    if not spec_url:
        result["controllo_pagina"] = KO
        result["dettaglio_pagina"] = "attributo spec-url assente o vuoto"
        debug(f"  -> titolo: {result['titolo']}")
        debug(f"  -> KO: {result['dettaglio_pagina']}")
        debug("STEP 2 - Controllo file: NON ESEGUITO")
        debug("STEP 3 - Controllo parsing: NON ESEGUITO")
        return result

    spec_url = urljoin(link, spec_url)  # se fosse relativo, lo rende assoluto
    result["spec_url"] = spec_url
    result["file_json"] = os.path.basename(urlparse(spec_url).path)
    debug(f"  -> titolo:   {result['titolo']}")
    debug(f"  -> spec-url: {spec_url}")
    debug(f"  -> file:     {result['file_json']}")

    # --- STEP 2: il file della specifica esiste ancora? -----------------------
    debug("STEP 2 - Controllo file spec-url (chiamata HTTP)")
    result["controllo_pagina"], result["dettaglio_pagina"] = check_spec_file(spec_url)
    debug(f"  -> {result['controllo_pagina']} ({result['dettaglio_pagina']})")
    if result["controllo_pagina"] != OK:
        debug("STEP 3 - Controllo parsing: NON ESEGUITO (file non raggiungibile)")
        return result  # senza file il controllo sul parsing non ha senso

    # --- STEP 3: <rapi-doc> ha fatto il parsing correttamente? ----------------
    debug("STEP 3 - Controllo parsing (elemento con i due bottoni)")
    result["controllo_parsing"], result["dettaglio_parsing"] = check_parsing(driver)
    debug(f"  -> {result['controllo_parsing']} ({result['dettaglio_parsing']})")
    return result


def check_page(driver, link):
    """
    Controlla un link e ritorna una LISTA di risultati:
    uno solo se la pagina non ha il menu versioni, uno per versione altrimenti.
    """
    # --- apertura della pagina ------------------------------------------------
    try:
        driver.get(link)
        WebDriverWait(driver, PAGE_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, RAPIDOC_SELECTOR))
        )
    except (TimeoutException, WebDriverException) as exc:
        result = new_result(link, "-")
        result["controllo_pagina"] = KO
        if isinstance(exc, TimeoutException):
            result["titolo"] = driver.title.strip()
            result["dettaglio_pagina"] = "elemento <rapi-doc> non trovato nella pagina"
        else:
            result["dettaglio_pagina"] = f"impossibile aprire la pagina: {type(exc).__name__}"
        debug(f"KO: {result['dettaglio_pagina']}")
        return [result]

    # --- STEP 0: c'e' il menu delle versioni? ---------------------------------
    dropdown = find_version_dropdown(driver)
    if dropdown is None:
        debug("Menu a tendina delle versioni NON trovato: pagina a versione singola")
        return [analyze_current_version(driver, link, "-")]

    debug("Menu a tendina delle versioni TROVATO")
    try:
        labels = list_versions(driver, dropdown)
    except (TimeoutException, WebDriverException) as exc:
        result = new_result(link, "?")
        result["controllo_pagina"] = KO
        result["dettaglio_pagina"] = f"menu versioni trovato ma voci non leggibili ({type(exc).__name__})"
        debug(f"  -> KO: {result['dettaglio_pagina']} (controlla OPTION_LOCATORS)")
        return [result]
    debug(f"  -> {len(labels)} versioni trovate: {labels}")

    # --- una analisi per ogni versione ----------------------------------------
    results = []
    seen_spec_urls = set()
    for i, label in enumerate(labels):
        debug(f"--- Versione {i + 1}/{len(labels)}: {label} ---")
        try:
            previous_spec_url = get_rapidoc(driver).get_attribute("spec-url")
        except WebDriverException:
            previous_spec_url = None

        # Se il menu mostra gia' questa versione (e il nome e' univoco) non serve selezionarla
        already_active = labels.count(label) == 1 and get_current_version_label(driver) == label
        if already_active:
            debug("  (versione gia' attiva nel menu: nessuna selezione necessaria)")
        else:
            try:
                select_version(driver, i)
            except (TimeoutException, WebDriverException) as exc:
                result = new_result(link, label)
                result["controllo_pagina"] = KO
                result["dettaglio_pagina"] = f"impossibile selezionare la versione ({type(exc).__name__})"
                debug(f"  -> KO: {result['dettaglio_pagina']}")
                results.append(result)
                continue
            # attendo che la pagina mostri la nuova versione (spec-url diverso)
            if not wait_spec_url_change(driver, previous_spec_url):
                debug("  (spec-url invariato dopo la selezione: selezione non avvenuta?)")

        result = analyze_current_version(driver, link, label)

        # Due versioni con lo stesso spec-url indicano che la selezione potrebbe non aver funzionato
        if result["spec_url"] and result["spec_url"] in seen_spec_urls:
            result["note"] = "spec-url uguale a quello di un'altra versione: verificare"
            debug(f"  ATTENZIONE: {result['note']}")
        seen_spec_urls.add(result["spec_url"])
        results.append(result)

    return results


# ----------------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------------

def print_table(results):
    """Stampa la tabella: link | versione | file json | controllo pagina | controllo parsing."""
    headers = ["link", "versione", "file json", "controllo pagina", "controllo parsing"]

    def with_detail(outcome, detail):
        return f"{outcome} ({detail})" if detail else outcome

    rows = [
        [
            r["link"],
            r["versione"],
            r["file_json"] or "-",
            with_detail(r["controllo_pagina"], r["dettaglio_pagina"]),
            with_detail(r["controllo_parsing"], r["dettaglio_parsing"]),
        ]
        for r in results
    ]
    # larghezza di ogni colonna = stringa piu' lunga
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    print("\n" + " | ".join(h.ljust(w) for h, w in zip(headers, widths)))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))
    print()


# def save_csv(results):
#     """Salva i risultati in output/risultati_<data_ora>.csv (separatore ';', apribile con Excel)."""
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     path = os.path.join(OUTPUT_DIR, f"risultati_{stamp}.csv")
#     with open(path, "w", newline="", encoding="utf-8-sig") as f:
#         writer = csv.DictWriter(f, fieldnames=list(results[0].keys()), delimiter=";")
#         writer.writeheader()
#         writer.writerows(results)
#     return path


def write_github_summary(results):
    """
    Su GitHub Actions scrive la tabella dei risultati nel riepilogo dell'esecuzione
    (pagina "Summary"). GitHub imposta la variabile d'ambiente GITHUB_STEP_SUMMARY con il
    percorso di un file: tutto il Markdown scritto li' viene mostrato nella pagina.
    In locale la variabile non esiste e la funzione non fa nulla.
    """
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    def cell(outcome):
        icon = {OK: "✅", KO: "❌"}.get(outcome, "⏭️")
        return f"{icon} {outcome}"

    ko_count = sum(KO in (r["controllo_pagina"], r["controllo_parsing"]) for r in results)
    lines = [
        "## Controllo pagine developer.pagopa.it",
        "",
        f"Controlli eseguiti: {len(results)} | con esito KO: {ko_count}",
        "",
        "| link | versione | file json | controllo pagina | controllo parsing |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in results:
            lines.append(
                f"| {r['link']} | {r['versione']} | {r['file_json'] or '-'} | "
                f"{cell(r['controllo_pagina'])} | "
                f"{cell(r['controllo_parsing'])} |"
            )
    with open(summary_path, "a", encoding="utf-8") as f:  # "a" = aggiunge in coda
        f.write("\n".join(lines) + "\n")


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------

def main():
    """Controlla tutti i link. Ritorna True se almeno un controllo e' KO."""
    links = read_links(LINKS_FILE)
    if not links:
        print(f"Nessun link trovato in {LINKS_FILE}")
        return False

    print(f"Trovati {len(links)} link da controllare...")
    driver = create_driver()
    results = []
    try:
        for i, link in enumerate(links, start=1):
            print(f"[{i}/{len(links)}] {link}")
            results.extend(check_page(driver, link))  # un risultato per ogni versione
    finally:
        driver.quit()  # chiude sempre il browser, anche in caso di errore

    print_table(results)
    # print(f"CSV salvato in: {save_csv(results)}")
    write_github_summary(results)

    return any(KO in (r["controllo_pagina"], r["controllo_parsing"]) for r in results)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
