"""Job application tracker: a small command-line tool."""

import csv
from pathlib import Path

DATA_FILE = Path("data/sample_applications.csv")


def load_applications(path):
    """Read all applications from a CSV file."""
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def list_applications(applications):
    """Print one line for each application."""
    for app in applications:
        print(f"{app['id']:>3}  {app['status']:<11}  {app['company']} - {app['role']}")


def main():
    applications = load_applications(DATA_FILE)
    list_applications(applications)


if __name__ == "__main__":
    main()