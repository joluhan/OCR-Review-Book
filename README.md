# LITRevu Web Application

## Introduction
LITRevu is a Django-based web application that allows users to publish and request book and article reviews. It enables users to find interesting reads based on community reviews and engage with other users by following their review activities.

## Requirements
- Python 3.x
- Django 3.1.x
- Other dependencies as listed in `requirements.txt`

## Installation
1. Clone the repository to your local machine.
```
https://github.com/joluhan/OCR-Review-Book.git
```
2. Navigate to the project directory.
3. Set up a Python virtual environment and activate it.
```
python -m venv env
source env/script/activate
```
4. Install the required dependencies using `pip`.
```
pip install -r requirements.txt
```
5. Apply migrations to set up the database schema.
```
python manage.py makemigrations
python manage.py migrate
```


## Database Setup
- Run the createsuperuser command to create a superuser account, which allows access to the Django admin interface.
```
python manage.py createsuperuser
```

## Running the Project
- Command to start the Django development server.
```
source env/script/activate
python manage.py runserver
```
- Access details for the web application (default is `http://127.0.0.1:8000/`).

## Additional Configuration
- Guide on setting up any additional services or environment variables.

## Usage
- Basic instructions on how to use the main features of the web application as outlined in the wireframes.
