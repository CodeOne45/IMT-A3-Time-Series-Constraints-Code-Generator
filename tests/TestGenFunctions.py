import json
from pathlib import Path
import unittest
import sys
from colorama import Fore, Style

sys.path.append('../gen')
import GeneratedFunctions

class TestGeneratedFunctions(unittest.TestCase):

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.suite = self.create_test_suite()

    def load_tests(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)["testTS"]

    def run_test(self, test_name, test_details):
        function = getattr(GeneratedFunctions, test_name)
        result = function(test_details["time_series"]).__str__()

        expected_result = (test_details["result"], test_details["time_series"], test_details["found"]).__str__()

        try:
            self.assertEqual(result, expected_result)
            print(Fore.GREEN + f"Pass: {test_name}")
        except AssertionError as e:
            print(Fore.RED + f"Fail: {test_name}\nResult   {result}\nExpected {expected_result}")

    def create_test_suite(self):
        suite = unittest.TestSuite()
        test_data = self.load_tests(self.file_path)

        for test_name, test_details in test_data.items():
            test_case = TestGeneratedFunctionsCase(self, test_name, test_details)
            suite.addTest(test_case)

        return suite


class TestGeneratedFunctionsCase(unittest.TestCase):
    def __init__(self, parent, test_name, test_details):
        super().__init__()
        self.parent = parent
        self.test_name = test_name
        self.test_details = test_details

    def runTest(self):
        with self.subTest(test_name=self.test_name):
            self.parent.run_test(self.test_name, self.test_details)


if __name__ == "__main__":
    unittest.main()
