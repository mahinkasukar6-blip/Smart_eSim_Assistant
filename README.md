# SMART eSIM 3.0 – Automated Tool Manager

An enterprise-style Python and Streamlit application developed for the eSim Winter Internship 2026.

## Overview

SMART eSIM 3.0 helps users monitor essential engineering tools and Python dependencies through a command-line tool manager and an interactive web dashboard.

## Features

- **Tool Manager:** Checks the availability and versions of Python, Git, NGSpice and KiCad.
- **Automated Installation:** Provides Linux package installation support for missing tools.
- **Dependency Checker:** Checks required Python modules and packages.
- **Enterprise Dashboard:** Displays system status and project readiness.
- **Tool Monitor:** Search and filter tools by installation status.
- **Installation Readiness:** Calculates an overall readiness score.
- **Analytics:** Visualizes tool and dependency status.
- **Activity Logs:** Records and displays system activity.
- **CSV Reports:** Allows users to download reports.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Git and GitHub
- Ubuntu / WSL

## Project Structure

```text
Smart_eSim_Assistant/
├── app.py
├── main.py
├── tool_checker.py
├── dependency_checker.py
├── README.md
├── .gitignore
└── activity.log
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/mahinkasukar6-blip/Smart_eSim_Assistant.git
```

2. Navigate to the project folder:

```bash
cd Smart_eSim_Assistant
```

3. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install streamlit pandas plotly
```

## Run the Application

Start the dashboard:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

Run the command-line tool manager:

```bash
python tool_checker.py
```

## Platform Notes

The automated software installation feature uses Ubuntu's `apt-get` package manager. Run it in Ubuntu or WSL with the required permissions.

## Project Goal

To simplify engineering tool management through automated checks, dependency monitoring, installation guidance and a centralized dashboard.

## Internship

**eSim Winter Internship 2026 – Task 5: Automated Tool Manager**

