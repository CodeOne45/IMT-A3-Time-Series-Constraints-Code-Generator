import gc
import tracemalloc
import json
import time
from tabulate import tabulate
import GeneratedFunctions

class PerformanceTests:
    def __init__(self, json, nbtest):
        self.json = json
        self.nbtest = nbtest
        self.functions = [
            'pos_max_max_bump_on_decreasing_sequence', 'pos_max_max_decreasing', 'pos_max_max_decreasing_sequence',
            'pos_max_max_dip_on_increasing_sequence', 'pos_max_max_increasing', 'pos_max_max_increasing_sequence',
            'pos_max_max_inflexion', 'pos_max_max_peak', 'pos_max_max_strictly_decreasing_sequence',
            'pos_max_max_strictly_increasing_sequence', 'pos_max_max_summit', 'pos_max_max_zigzag',
            'pos_max_min_bump_on_decreasing_sequence', 'pos_max_min_decreasing', 'pos_max_min_decreasing_sequence',
            'pos_max_min_dip_on_increasing_sequence', 'pos_max_min_gorge', 'pos_max_min_increasing',
            'pos_max_min_increasing_sequence', 'pos_max_min_inflexion', 'pos_max_min_strictly_decreasing_sequence',
            'pos_max_min_strictly_increasing_sequence', 'pos_max_min_valley', 'pos_max_min_zigzag',
            'pos_min_max_bump_on_decreasing_sequence', 'pos_min_max_decreasing', 'pos_min_max_decreasing_sequence',
            'pos_min_max_dip_on_increasing_sequence', 'pos_min_max_increasing', 'pos_min_max_increasing_sequence',
            'pos_min_max_inflexion', 'pos_min_max_peak', 'pos_min_max_strictly_decreasing_sequence',
            'pos_min_max_strictly_increasing_sequence', 'pos_min_max_summit', 'pos_min_max_zigzag',
            'pos_min_min_bump_on_decreasing_sequence', 'pos_min_min_decreasing', 'pos_min_min_decreasing_sequence',
            'pos_min_min_dip_on_increasing_sequence', 'pos_min_min_gorge', 'pos_min_min_increasing',
            'pos_min_min_increasing_sequence', 'pos_min_min_inflexion', 'pos_min_min_strictly_decreasing_sequence',
            'pos_min_min_strictly_increasing_sequence', 'pos_min_min_valley', 'pos_min_min_zigzag'
        ]

# ...

    def cpu_charge(self):
        data = json.load(open(self.json))
        print('\nTest n°' + self.nbtest.__str__() + '\nNombre de lignes à traiter: ' + len(data).__str__())
        print('-' * 70)

        results = []
        total_execution_time = 0


        for function in self.functions:
            to_run = getattr(GeneratedFunctions, function)
            start = time.time()
            tracemalloc.start()
            gc.collect()
            before = tracemalloc.take_snapshot()
            to_run(data)
            after = tracemalloc.take_snapshot()
            stop = time.time()

            tracemalloc.stop()

            tmps_execution = stop - start

            stats = after.compare_to(before, 'lineno')
            stat = stats[:1].__str__().split('>')

            result = {
                "Function": function,
                "Memory Increase": stat[2].strip(),
                "Execution Time": f'{tmps_execution:.2f}s',
            }
            results.append(result)

            total_execution_time += tmps_execution


        headers = ["Function", "Memory Increase", "Execution Time"]
        # Ensure results is a list of dictionaries
        table = tabulate([result.values() for result in results], headers=headers, tablefmt="fancy_grid")

        print(table)
        print("Total execution time: " + f'{total_execution_time:.2f}s')

# ...


# Uncomment the following lines if you want to run the performance tests directly from this file.
# performance_tests = PerformanceTests('Json/accenture.json', 1)
# performance_tests.cpu_charge()
