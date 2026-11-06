"""Job application tracker: a small command-line tool."""

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

DATA_FILE = Path("data/applications.csv")
SAMPLE_FILE = Path("data/sample_applications.csv")
FIELDS = ["id", "company", "role", "source", "status", "applied_date", "notes"]
STATUSES = ["Applied", "In process", "Offer", "Rejected", "Withdrawn"]


def active_file():
    """Use the private data file if it exists, otherwise the sample file."""
    return DATA_FILE if DATA_FILE.exists() else SAMPLE_FILE


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


def next_id(applications):
    """Return the next free application number."""
    return max((int(app["id"]) for app in applications), default=0) + 1


def add_application(path, company, role, source, notes):
    """Save a new application and return it."""
    is_new_file = not path.exists()
    applications = [] if is_new_file else load_applications(path)
    application = {
        "id": next_id(applications),
        "company": company,
        "role": role,
        "source": source,
        "status": "Applied",
        "applied_date": date.today().isoformat(),
        "notes": notes,
    }
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, lineterminator="\n")
        if is_new_file:
            writer.writeheader()
        writer.writerow(application)
    return application


def save_applications(path, applications):
    """Write all applications back to the CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(applications)


def update_status(path, application_id, status):
    """Change the status of one application and return it."""
    applications = load_applications(path) if path.exists() else []
    for app in applications:
        if app["id"] == application_id:
            app["status"] = status
            save_applications(path, applications)
            return app
    return None


def build_parser():
    """Define the commands the tool accepts."""
    parser = argparse.ArgumentParser(description="Track job applications.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="show all applications")
    subparsers.add_parser("stats", help="show totals by status")
    add_parser = subparsers.add_parser("add", help="add a new application")
    add_parser.add_argument("company", help="company name")
    add_parser.add_argument("role", help="job title")
    add_parser.add_argument("--source", default="", help="where you found the job")
    add_parser.add_argument("--notes", default="", help="a short note")
    update_parser = subparsers.add_parser("update", help="change an application status")
    update_parser.add_argument("id", help="application number")
    update_parser.add_argument("status", choices=STATUSES, help="new status")
    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "add":
        application = add_application(DATA_FILE, args.company, args.role, args.source, args.notes)
        print(f"Added application {application['id']}: {application['company']}")
    elif args.command == "list":
        list_applications(load_applications(active_file()))
    elif args.command == "stats":
        show_stats(load_applications(active_file()))
    elif args.command == "update":
        application = update_status(DATA_FILE, args.id, args.status)
        if application:
            print(f"Updated application {application['id']}: {application['status']}")
        else:
            print(f"No application found with id {args.id}")


if __name__ == "__main__":
    main()