import json
import argparse
from glob import glob 
from TransducerGenerator import *



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_files', nargs='+', required=True)
    # get all files names from input_files directory

    input_transducers_files = []
    args = parser.parse_args()
    for arg in args.input_files:
        input_transducers_files += glob(arg)

    transducers = {}
    for file in input_transducers_files:
        with open(file) as f:
            try:
                transducers.update(json.load(f))
                print(json.load(f))
            except json.decoder.JSONDecodeError as exc:
                print(exc)
    # decorationTables.json'
    tables = json.load(open('src/decorationTables.json'))["tables"]["decoration"]
    #convert transducers dic to json object
    transducerGenerator = TransducerGenerator(transducers, tables)
    transducerGenerator.generate_functions()






