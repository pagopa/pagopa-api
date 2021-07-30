import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("jsonfile", help="json string")
parser.add_argument("type", help="type a=all p=only package c=only common-xml")
args = parser.parse_args()

with open(args.jsonfile) as f:
    data = json.load(f)
    pkg_version = data[0]["version"]

    data_for_common_xml_vers = [x for x in data if x["name"] == "re-feeder"]
    commmon_xml_vers = (list(filter(lambda x: x.startswith("eu.sia.pagopa:common-xml"),
                                    data_for_common_xml_vers[0]["libraryDependencies"]))[0].split(":")[2])

    if (args.type == "a"):
        print("pkg_version ", pkg_version,
              " common_xml ", commmon_xml_vers)
    elif (args.type == "p"):
        print(pkg_version)
    elif (args.type == "c"):
        print(commmon_xml_vers)
