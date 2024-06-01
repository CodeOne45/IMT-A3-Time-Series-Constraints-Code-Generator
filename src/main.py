import json
import argparse
from glob import glob 
from FunctionsGenerator import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_files', nargs='+', required=True)
    args = parser.parse_args()

    input_transducers_files = []
    for arg in args.input_files:
        input_transducers_files += glob(arg)

    transducers = {}
    for file in input_transducers_files:
        try:
            with open(file) as f:
                content = f.read().strip()
                if content:  # Check if the file is not empty
                    transducers.update(json.loads(content))
                else:
                    print(f"Warning: The file {file} is empty.")
        except json.decoder.JSONDecodeError as exc:
            print(f"Error decoding JSON from file {file}: {exc}")

    # Load decoration tables
    try:
        with open('src/decorationTables.json') as tables_file:
            tables_data = json.load(tables_file)
            tables = tables_data["tables"]["decoration"]
            features = tables_data["tables"]["features"]
            aggregators = tables_data["tables"]["aggregators"]

    except json.decoder.JSONDecodeError as exc:
        print(f"Error decoding JSON from decorationTables.json: {exc}")
        tables = {}

    # Initialize TransducerGenerator if transducers and tables are properly loaded
    if transducers and tables:
        transducerGenerator = FunctionsGenerator(transducers, tables, aggregators, features)
        transducerGenerator.generate_functions()
        print("Success: Generated functions.")
    else:
        print("Error: Transducers or decoration tables are not properly loaded.")





