import json
import sys
import unittest
from pathlib import Path

sys.path.append('../gen')
import GeneratedFunctions


class TestGeneratedFunctions(unittest.TestCase):
    def load_tests(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)["testTS"]

    def run_test(self, test_name, test_details):
        function = getattr(GeneratedFunctions, test_name)
        result = function(test_details["time_series"]).__str__()

        expected_result = (test_details["result"], test_details["time_series"], test_details["found"]).__str__()

        self.assertEqual(result, expected_result, f"{test_name} is KO\nResult   {result}\nExpected {expected_result}")

    def test_generated_functions(self):
        file_path = Path('data/tsFunctionsTest.json')

        if not file_path.is_file():
            self.fail(f"Error: The file {file_path} does not exist.")

        test_data = self.load_tests(file_path)

        for test_name, test_details in test_data.items():
            with self.subTest(test_name=test_name):
                self.run_test(test_name, test_details)


if __name__ == "__main__":
    unittest.main()
