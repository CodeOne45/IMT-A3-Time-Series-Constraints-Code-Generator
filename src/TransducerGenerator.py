# TransducerGenerator.py

import yaml
import re
from Enums.Patterns import Patterns
from Enums.Semantics import Semantics
from Enums.Aggregators import Aggregators
import json



class TransducerGenerator:
    def __init__(self, transducers, tablesConfig):
        self.transducers = transducers
        self.decorationTables = tablesConfig

        self.features = {
            "max": {
                "neutral_f": "-inf",
                "min_f": "-inf",
                "max_f": "inf",
                "phi_f": "max",
                "delta_f": "x_i"
            },
            "min": {
                "neutral_f": "inf",
                "min_f": "-inf",
                "max_f": "inf",
                "phi_f": "min",
                "delta_f": "x_i"
            },
            "surf": {
                "neutral_f": "0",
                "min_f": "-inf",
                "max_f": "inf",
                "phi_f": "add",
                "delta_f": "x_i"
            },
            "width": {
                "neutral_f": "0",
                "min_f": "0",
                "max_f": "inf",
                "phi_f": "add",
                "delta_f": "1"
            }
        }

        self.aggregators = {
            "Max": {
                "default_g_f": "min_f"
            },
            "Min": {
                "default_g_f": "max_f"
            }
        }


    def generate_functions(self):
        for transducer in self.transducers:
            self.generate_transducer_function(transducer)

    def generate_transducer_function(self, transducers):
        f = open(f"GeneratedFunctions.py", "w")
        # Writing imports
        self.write_imports(f)

        for aggregator in self.aggregators :
            # Iterating of features
            for feature in self.features:
                g = aggregator.lower()
                phi_f = self.features[feature]["phi_f"]
                for pattern in self.transducers:
                    function_name = f"pos_{aggregator.lower()}_{feature}_{pattern}"
                    f.write(f"def {function_name}(time_series):\n")
                    self.write_transducer_function_body(f, g, phi_f, pattern, aggregator, feature)
                    f.write("\n\n")

        f.close()

    def write_imports(self, f):
        f.write("from math import inf\n")
        f.write("from Enums.Patterns import Patterns\n")
        f.write("from GuardValue import GuardValue\n")
        f.write("from TimeSeriesParser import *\n\n\n")


    def write_transducer_function_body(self, f, g, phi_f, pattern, aggregator_data, feature_data):
        # Writing the time_series to signature function call line
        f.write("    signature = time_series_to_signature_parser(time_series)\n")
        # Writing the signature to semantics function call line
        f.write(f"    semantics = signature_to_semantic(signature, Patterns.{pattern.upper()})\n")
        # Declaring the default_g_f constant
        f.write(f"    default_g_f = {float(self.features[feature_data][(self.aggregators[aggregator_data]['default_g_f'])]).__str__()} \n")
        # Declaring the neutral_f constant
        f.write(f"    neutral_f = {float(self.features[feature_data]['neutral_f']).__str__()} \n")
        f.write("\n")

        # Declaring accumulators
        f.write("    R = default_g_f\n    C = default_g_f\n    D = neutral_f\n\n")

        # Declaring guard tables
        f.write(
            "    at = [GuardValue(0)] * len(time_series)\n"
            "    ct = [GuardValue(0)] * len(time_series)\n"
            "    f = [GuardValue(0)] * len(time_series)\n\n")

        # Declaring the i counter for getting the current value in the series
        f.write("    i = 0\n\n")

        f.write("    for word in semantics:\n")

        # Declaring delta_f which sometimes is equal to the current position in the time series
        if self.features[feature_data]["delta_f"] == "x_i":
            f.write("        delta_f = time_series[i]\n")
            f.write("        delta_f_1 = time_series[i + 1]\n")
        else:
            f.write(f"        delta_f = {self.features[feature_data]['delta_f']}\n")

        # Writing the different cases for each semantic word
        f.write("        match word:\n")
        for word in Semantics:
            after_value = self.transducers[pattern]["after"].__str__()
            f.write(f"            case Semantics.{word}:\n")
            f.write(self.prepare_guard_lines(word, after_value, g, phi_f, 4, feature_data) + "\n")
            operations = self.decorationTables["after" + after_value][word.value]
            for operation in operations:
                f.write(f"                {self.prepare_operation_line(operation, g, phi_f)}\n\n")

        f.write("        i += 1 \n\n")

        # Guard end conditions
        f.write("    f[len(time_series) - 1] = GuardValue(0)\n")
        f.write(f"    if C {'<' if aggregator_data == Aggregators.MIN.value else '>'} R:\n")
        f.write("        ct[len(time_series) - 1] = GuardValue(1)\n")
        f.write("        at[len(time_series) - 1] = GuardValue(0)\n")
        f.write(f"    elif (C == R) & (R == default_g_f):\n")
        f.write("        ct[len(time_series) - 1] = GuardValue(0)\n")
        f.write("        at[len(time_series) - 1] = GuardValue(0)\n")
        f.write(f"    elif (C == R) & (R != default_g_f):\n")
        f.write("        ct[len(time_series) - 1] = GuardValue(1)\n")
        f.write("        at[len(time_series) - 1] = GuardValue(1)\n")
        f.write(f"    elif R {'<' if aggregator_data == Aggregators.MIN.value else '>'} C:\n")
        f.write("        ct[len(time_series) - 1] = GuardValue(0)\n")
        f.write("        at[len(time_series) - 1] = GuardValue(1)\n\n")

        # Writing return statement
        f.write(f"\n    return {g}(R,C), time_series, f\n")
        f.write("\n\n")

    def prepare_operation_line(self, operation, g, phi_f, sub_op=False):
        line = ""
        
        # Beginning of the code line generated (if not a sub operation)
        if not sub_op:
            line = line + operation["acc"] + " = "

        # Getting the second value, if variable get the name, if other operation preparing it
        value2 = ""
        if "value2" in operation:
            if not isinstance(operation["value2"], str):
                value2 = f"({self.prepare_operation_line(operation['value2'], g, phi_f, True)})"
            else:
                if value2 == "inf" or value2 == "-inf":
                    value2 = f"float({operation['value2']})"
                else:
                    value2 = operation["value2"]

        # Getting the first value and the operator
        value1 = ""
        if value1 == "inf" or value1 == "-inf":
            value1 = f"float({operation['value1']})"
        else:
            value1 = operation["value1"]
        operator = operation["operator"]

        # Finishing line writing
        if operator == "affect":
            line = line + value1
        elif operator == "g":
            operator = g
            line = line + f"{operator}({value1}, {value2})"
        elif operator == "phi_f":
            operator = phi_f
            line = line + f"{operator}({value1}, {value2})"

        return line

    def prepare_guard_lines(self, semantic, after_value, g, phi_f, nb_tab, feature_data):
        lines = ""
        # Defining a variable to indent the code block according to the level it will be written in the final file
        tab = nb_tab * "    "
        # Getting the appropriate part of the decoration table
        guard_table = self.decorationTables["guard"]["after" + after_value]
        # Iteration on the different cases for the semantic word
        for case in guard_table[semantic.value]:
            # Checking if there is a condition for this case to execute operation(s)
            condition = "condition" in case
            if condition:
                condition = f"if {case['condition']}:"
                if g == "max":
                    condition = condition.replace("<g", ">")  # Replacing <g by the > operator
                elif g == "min":
                    condition = condition.replace("<g", "<")  # Replacing <g by the < operator
                condition = condition.replace("phi_f", phi_f)  # Replacing phi_f by the appropriate function
                lines = lines + tab + condition + "\n"
            # Iterating on operations lines
            for operation in case["operations"]:
                # Indenting if there is a condition to the operation
                if condition:
                    lines = lines + "    "
                var = operation["var"]  # Getting the variable to change
                value = operation["value"]  # Value to affect to the variable
                # If the value is an int we use the value form of GuardValue, if not we use the pointer form
                if isinstance(value, int):
                    lines = lines + tab + f"{var} = GuardValue({value.__str__()})" + "\n"
                else:
                    # Getting separately the name of the table to affect and the index
                    match = re.search(r"(at|ct|f)\[(i\+1|i)\]", value)
                    if not (match is None):
                        lines = lines + tab + f"{var} = GuardValue(float(inf), {match.group(1)}, {match.group(2)}, \"{match.group(1)}\")" + "\n"
        return lines

