"""Job application tracker: a small command-line tool."""

import argparse
import csv
from collections import Counter
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


def show_stats(applications):
    """Print the total and the number of applications for each status."""
    counts = Counter(app["status"] for app in applications)
    print(f"Total applications: {len(applications)}")
    for status, count in counts.most_common():
        print(f"{status:<11}  {count}")


def build_parser():
    """Define the commands the tool accepts."""
    parser = argparse.ArgumentParser(description="Track job applications.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="show all applications")
    subparsers.add_parser("stats", help="show totals by status")
    return parser


def main():
    args = build_parser().parse_args()
    applications = load_applications(DATA_FILE)
    if args.command == "list":
        list_applications(applications)
    elif args.command == "stats":
        show_stats(applications)


if __name__ == "__main__":
    main()