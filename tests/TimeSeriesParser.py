import json
from Enums.Semantics import Semantics

def time_series_to_signature_parser(time_series):
    """
    Convert a time series into a signature based on the trends between consecutive values.

    Args:
    - time_series (list): List representing the time series data.

    Returns:
    - list: Signature list indicating the trends ('>', '<', or '=') between consecutive values.
    """
    signature = []
    for i in range(len(time_series) - 1):
        if time_series[i] > time_series[i + 1]:
            signature.append(">")
        elif time_series[i] < time_series[i + 1]:
            signature.append("<")
        else:
            signature.append("=")
    return signature

def signature_to_semantic(signature, pattern):
    """
    Convert a time series signature into a list of semantic words based on a specified pattern.

    Args:
    - signature (list): Signature list indicating the trends ('>', '<', or '=') between consecutive values.
    - pattern (Semantics): Enum representing the requested pattern.

    Returns:
    - list: List of semantic words corresponding to the provided signature and pattern.
    """
    res = []
    graph = json.load(open('Graphs.json'))["graphs"][pattern.value]
    current_state = graph["entryState"]
    states = graph["states"]

    for symbol in signature:
        transitions = states[current_state]["transitions"]
        for transition in transitions:
            if symbol == transition["consume"]:
                res.append(Semantics(transition["produce"]))
                current_state = transition["next"]
                break

    return res
