from math import inf
from Enums.Patterns import Patterns
from Enums.Aggregators import Aggregators
from GuardValue import GuardValue
from TimeSeriesParser import *


def max_function (a,b):
    return max(a,b)

def min_function (a,b):
    return min(a,b)

def add_function (a,b):
    return int(a) + int(b)

def add_function (a,b):
    return int(a) + int(b)

operator_mapping = {
    "Min": lambda x, y: x < y,
    "Max": lambda x, y: x > y,
}

def applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after): 
    i = 0

    delta_x_i = True if delta_f == "x_i" else False

    g = aggregator_data.lower() + "_function"

    for word in semantics:
        if delta_x_i == True:
            delta_f = time_series[i]
            delta_f_1 = time_series[i + 1]
        else:
           delta_f = delta_f
        match word:
            case Semantics.FOUND:
                if after == 0:
                    ct[i] = GuardValue(0)
                    f[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    C = globals()[operetor](delta_f_1, (    globals()[operetor](D, delta_f)))

                    D = neutral_f

                if after == 1:
                    ct[i] = GuardValue(0)
                    f[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    C = globals()[operetor](D, delta_f)

                    D = neutral_f

            case Semantics.FOUND_END:
                if after == 0:
                    if operator_mapping[aggregator_data](globals()[operetor](globals()[operetor](D,delta_f),delta_f_1), R):
                            f[i] = GuardValue(float(inf), ct, i, "ct")
                            at[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                    if globals()[operetor](globals()[operetor](D,delta_f),delta_f_1) == R:
                            f[i] = GuardValue(float(inf), at, i+1, "at")
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                            at[i] = GuardValue(float(inf), at, i+1, "at")
                    if operator_mapping[aggregator_data](R, globals()[operetor](globals()[operetor](D,delta_f),delta_f_1)):
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(0)
                            at[i] = GuardValue(float(inf), at, i+1, "at")

                    R = globals()[g](R, (    globals()[operetor](delta_f_1, (    globals()[operetor](D, delta_f)))))

                    D = neutral_f

                if after == 1:
                    if operator_mapping[aggregator_data](globals()[operetor](D,delta_f), R ):
                            f[i] = GuardValue(float(inf), ct, i, "ct")
                            at[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                    if globals()[operetor](D,delta_f) == R:
                            f[i] = GuardValue(float(inf), at, i+1, "at")
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                            at[i] = GuardValue(float(inf), at, i+1, "at")
                    if operator_mapping[aggregator_data](R, globals()[operetor](D,delta_f)):
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(0)
                            at[i] = GuardValue(float(inf), at, i+1, "at")

                    R = globals()[g](R, (    globals()[operetor](D, delta_f)))

                    D = neutral_f

            case Semantics.MAYBE_BEFORE:
                if after == 0:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = globals()[operetor](D, delta_f)

                if after == 1:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = globals()[operetor](D, delta_f)

            case Semantics.OUT_RESET:
                if after == 0:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = neutral_f

                if after == 1:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = neutral_f

            case Semantics.IN:
                if after == 0:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    C = globals()[operetor](C, (    globals()[operetor](D, delta_f_1)))

                    D = neutral_f

                if after == 1:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    C = globals()[operetor](C, (    globals()[operetor](D, delta_f)))

                    D = neutral_f

            case Semantics.MAYBE_AFTER:
                if after == 0:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = globals()[operetor](D, delta_f_1)

                if after == 1:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                    D = globals()[operetor](D, delta_f)

            case Semantics.OUT_AFTER:
                if after == 0:
                    if operator_mapping[aggregator_data](C, R):
                            f[i] = GuardValue(0)
                            at[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                    if C == R:
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                            at[i] = GuardValue(float(inf), at, i+1, "at")
                    if operator_mapping[aggregator_data](R, C):
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(0)
                            at[i] = GuardValue(float(inf), at, i+1, "at")

                    R = globals()[g](R, C)

                    C = default_g_f

                    D = neutral_f

                if after == 1:
                    if operator_mapping[aggregator_data](C, R ):
                            f[i] = GuardValue(0)
                            at[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                    if C == R:
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(float(inf), at, i+1, "at")
                            at[i] = GuardValue(float(inf), at, i+1, "at")
                    if operator_mapping[aggregator_data](R, C):
                            f[i] = GuardValue(0)
                            ct[i] = GuardValue(0)
                            at[i] = GuardValue(float(inf), at, i+1, "at")

                    R = globals()[g](R, C)

                    C = default_g_f

                    D = neutral_f

            case Semantics.OUT:
                if after == 0:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

                if after == 1:
                    f[i] = GuardValue(0)
                    ct[i] = GuardValue(float(inf), ct, i+1, "ct")
                    at[i] = GuardValue(float(inf), at, i+1, "at")

        i += 1 

    f[len(time_series) - 1] = GuardValue(0)
    if C < R if aggregator_data == Aggregators.MIN.value else C > R:
        ct[len(time_series) - 1] = GuardValue(1)
        at[len(time_series) - 1] = GuardValue(0)
    elif (C == R) & (R == default_g_f):
        ct[len(time_series) - 1] = GuardValue(0)
        at[len(time_series) - 1] = GuardValue(0)
    elif (C == R) & (R != default_g_f):
        ct[len(time_series) - 1] = GuardValue(1)
        at[len(time_series) - 1] = GuardValue(1)
    elif R < C if aggregator_data == Aggregators.MIN.value else R > C:
        ct[len(time_series) - 1] = GuardValue(0)
        at[len(time_series) - 1] = GuardValue(1)


    return globals()[g](R,C), time_series, f


def max_max_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_max_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = -inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_min_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = -inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_surf_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = -inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def max_width_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = 0.0 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Max"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_max_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = inf 
    neutral_f = -inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "max_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_min_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = inf 
    neutral_f = inf 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "min_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_surf_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "x_i"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_bump_on_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.BUMP_ON_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_decreasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_decreasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DECREASING_TERRACE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_dip_on_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.DIP_ON_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_gorge(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.GORGE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_increasing(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_increasing_terrace(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INCREASING_TERRACE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_inflexion(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.INFLEXION)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_peak(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PEAK)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLAIN)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PLATEAU)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_proper_plain(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLAIN)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_proper_plateau(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.PROPER_PLATEAU)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_steady(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_steady_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STEADY_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_strictly_decreasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_DECREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_strictly_increasing_sequence(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.STRICTLY_INCREASING_SEQUENCE)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 0

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_summit(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.SUMMIT)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_valley(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.VALLEY)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


def min_width_zigzag(time_series):
    signature = time_series_to_signature_parser(time_series)
    semantics = signature_to_semantic(signature, Patterns.ZIGZAG)
    default_g_f = inf 
    neutral_f = 0.0 

    R = default_g_f
    C = default_g_f
    D = neutral_f

    at = [GuardValue(0)] * len(time_series)
    ct = [GuardValue(0)] * len(time_series)
    f = [GuardValue(0)] * len(time_series)

    operetor = "add_function"
    delta_f = "1"
    aggregator_data = "Min"

    after = 1

    return applyDecoretor(time_series, semantics, at, ct, f, R, C, D, default_g_f, delta_f, neutral_f, operetor, aggregator_data, after)


