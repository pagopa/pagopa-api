import csv
import json
import sys

csv_filename = sys.argv[1]
out_filename = sys.argv[2]

# All expected fields in xlsx columns
all_fields = {
    0: 'CODICE TIPO ENTE CREDITORE',
    1: 'TIPO ENTE CREDITORE',
    2: 'Progressivo Macro Area per Ente Creditore',
    3: "NOME MACRO AREA",
    4: "DESCRIZIONE MACRO AREA CODICE",
    5: "CODICE TIPOLOGIA SERVIZIO",
    6: "TIPO SERVIZIO",
    7: "Motivo Giuridico della riscossione",
    8: "DESCRIZIONE TIPO SERVIZIO",
    9: "VERSIONE TASSONOMIA",
    10: "DATI SPECIFICI DI INCASSO",
    11: "DATA INIZIO VALIDITA",
    12: "DATA FINE VALIDITA",
}

#relevant_fields_index = [6, 8, 9, 10, 11, 12]
relevant_fields_index = range(0, 12)
relevant = dict((k, all_fields[k]) for k in relevant_fields_index)

data = []
with open(csv_filename, "r") as infile:
    reader = csv.reader(infile)
    # skip the headers
    next(reader, None)  
    for row in reader:
        # skip lines in CSV that "resulted empty" (eg: ,,,,)
        if all(len(f) == 0 for f in row):
            continue
        full_elem = dict(zip(all_fields.values(), row))
        wanted_elem = dict((k, full_elem[k]) for k in relevant.values())
        data.append(wanted_elem)

with open(out_filename, "w") as outfile:
    json.dump(data, outfile)
