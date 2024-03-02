# Idea Inlet

## Introduction

Ideal Inlet is a comprehensive online platform designed to streamline the process of submitting and managing abstracts for various events, conferences, publications, and academic endeavors. It provides a user-friendly interface for both authors and organizers, facilitating seamless communication and efficient handling of abstract submissions.

## Features

* Author-friendly interface: Easy submission of abstracts, including title, keywords, author information, and file uploads.
* Organizer dashboard: Manage submissions, review progress, communicate with authors, and download relevant data.
* Streamlined workflow: Efficient review processes, automated notifications, and centralized data management.
* Customizable settings: Organizers can tailor submission criteria, review forms, and access controls.
* Secure platform: Ensures data privacy and integrity for authors and organizers.

## Installation

Prerequisites:
* Python 3.6 or later
* pip (package manager for Python)

1. Clone the repository:

```bash
    git clone https://github.com/Franklinson/ideainlet.git
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv ideal_inlet_env
source ideal_inlet_env/bin/activate
```

3. Install dependencies:

```bash
cd idealinlet
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

This will start the Django development server, accessible by default at http://127.0.0.1:8000/.

## Demo

A live demo of the project can be found [here](https://youtu.be/aocrUDK1elk).

## Authors

- [Franklin Etsey Hassey](https://github.com/Franklinson)
- [Isabel Kikuvi](https://github.com/Isabel-Kikuvi)
