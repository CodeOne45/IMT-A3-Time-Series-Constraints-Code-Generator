import unittest
from pathlib import Path
from TestGenFunctions import TestGeneratedFunctions
from TestPerfprmance import PerformanceTests

if __name__ == "__main__":
    file_path = Path('data/tsFunctionsTest.json')

    test_instance = TestGeneratedFunctions(file_path)

    unittest.TextTestRunner().run(test_instance.suite)
    # Create an instance of the PerformanceTests class
    performance_tests = PerformanceTests('data/covid_new_patients_in_intensive_care.json', 1)

    # Run the performance tests
    performance_tests.cpu_charge()

