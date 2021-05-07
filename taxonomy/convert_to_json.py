import csv
import json
import sys
import codecs

csv_filename = sys.argv[1]
out_filename = sys.argv[2]

# All expected fields in xlsx columns
all_fields = {
    0: 'CODICE TIPO ENTE CREDITORE',
    1: 'TIPO ENTE CREDITORE',
    2: 'Progressivo Macro Area per Ente Creditore',
    3: "NOME MACRO AREA",
    4: "DESCRIZIONE MACRO AREA",
    5: "CODICE TIPOLOGIA SERVIZIO",
    6: "TIPO SERVIZIO",
    7: "Motivo Giuridico della riscossione",
    8: "DESCRIZIONE TIPO SERVIZIO",
    9: "VERSIONE TASSONOMIA",
    10: "DATI SPECIFICI DI INCASSO",
    11: "DATA INIZIO VALIDITA",
    12: "DATA FINE VALIDITA",
}

relevant_fields_index = range(0, 13)
relevant = dict((k, all_fields[k]) for k in relevant_fields_index)

# Collect all data from CSV
data = []
with codecs.open(csv_filename, 'r', 'utf-8') as infile:
    rows = csv.reader(infile)
    # skip the headers
    next(rows, None)
    for row in rows:
        # skip lines in CSV that "resulted empty" (eg: ,,,,)
        if all(len(f) == 0 for f in row):
            continue
        full_elem = dict(zip(all_fields.values(), row))
        wanted_elem = dict((k, full_elem[k]) for k in relevant.values())
        data.append(wanted_elem)

# Extract info for Macro Area
macro_area = {}
for d in data:
    myid = d['CODICE TIPO ENTE CREDITORE'] + \
        d['Progressivo Macro Area per Ente Creditore']
    nome = d['NOME MACRO AREA']
    desc = d['DESCRIZIONE MACRO AREA']
    if nome:
        macro_area[myid] = {'nome': nome, 'desc': desc}

# Adjust Macro Area missing info
for d in data:
    if not d['NOME MACRO AREA']:
        temp_id = d['CODICE TIPO ENTE CREDITORE'] + \
            d['Progressivo Macro Area per Ente Creditore']
        d['NOME MACRO AREA'] = macro_area[temp_id]['nome']
        d['DESCRIZIONE MACRO AREA'] = macro_area[temp_id]['desc']

# Reverse on JSON output
with codecs.open(out_filename, 'w', 'utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
