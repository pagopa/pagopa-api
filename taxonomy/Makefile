TASSONOMIA_SERVIZI_URL = 'https://docs.google.com/uc?export=download&id=13xOd__Qd4pwKHr3wjE-73NAB2O7UKmIt'

tassonomia.xlsx:
	mkdir -p ./tmp
	wget --no-check-certificate $(TASSONOMIA_SERVIZI_URL) -O ./tmp/tassonomia.xlsx

tassonomia.csv:
	xlsx2csv ./tmp/tassonomia.xlsx > ./tmp/tassonomia.csv

tassonomia.json:
	python convert_to_json.py ./tmp/tassonomia.csv ./tmp/tassonomia.json

copy_tassonomia:
	cp ./tmp/tassonomia.json .

all: tassonomia.xlsx tassonomia.csv tassonomia.json copy_tassonomia clean

clean:
	rm -rf ./tmp

.PHONY: tassonomia.xlsx tassonomia.csv tassonomia.json clean