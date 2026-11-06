# Job Application Tracker

A small command-line tool for tracking job applications. It saves each application in a CSV file and shows a list or a summary by status.

I am tracking more than 180 job applications, so I started this project to make that work easier.

## Who it is for

Job seekers who want a simple and private way to track applications without an online account.

## Built with

Python 3 and its standard library: `argparse`, `csv`, `collections`, `datetime` and `pathlib`. No external packages are needed.

## How to run

```bash
git clone https://github.com/bekir35-on/job-application-tracker.git
cd job-application-tracker
python3 tracker.py list
```

## Commands

| Command | What it does |
|---|---|
| `python3 tracker.py list` | Shows all applications |
| `python3 tracker.py stats` | Shows the total and the number for each status |
| `python3 tracker.py add "Company" "Role" --source "Reed" --notes "Short note"` | Saves a new application |
| `python3 tracker.py update 1 "In process"` | Changes the status of an application |

## Data and privacy

`data/sample_applications.csv` contains made-up examples.

New applications are saved to `data/applications.csv`. This file is listed in `.gitignore`, so your real data stays on your computer.

## Planned work


- Filter the list by status
- Import applications from an existing CSV file
- Export a PDF report
- Add follow-up reminders


## License

MIT