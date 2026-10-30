# CivicDesk Mini

A Python web application for submitting and tracking fictional
neighbourhood service requests.

Independent portfolio demo. Not affiliated with Dubai Government
or connected to any real government service.

## Features

- Submit a request with a title, category, location, and description.
- View saved requests, with the newest first.
- Update a request to Submitted, In progress, or Resolved.
- Preserve requests and statuses after refreshing or restarting.

## Technologies

- Python and Flask: application logic and web routes.
- SQLite: persistent storage.
- HTML and Jinja: pages and request table.
- CSS: styling and layout.

## Run locally on Windows

Install Python, download the project, and open a terminal
inside the project folder.

Run these commands one at a time:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser.

The database is created automatically on the first run.
Keep the terminal open while using the app.
Press Ctrl+C to stop it.

## Try the app

1. Submit a request using fictional details.
2. Return to the home page.
3. Change its status and click Save.
4. Refresh to confirm that the change remains saved.

## Current scope

This is a local, single-user learning project.
Accounts, notifications, and government integrations are outside
the current version.

