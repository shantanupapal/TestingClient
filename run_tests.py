# run_tests.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test_suite", default="regression")
parser.add_argument("--env", default="staging")

args = parser.parse_args()

print(f"Running test suite: {args.test_suite}")
print(f"Environment: {args.env}")
