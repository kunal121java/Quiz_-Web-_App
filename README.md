# Quiz_-Web-_App


This is a Django-based Quiz web application that allows users to register, login, take quizzes on various subjects, and view their quiz results.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

## Installation and Setup

1. Clone the repository to your local machine:

   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
(Optional but recommended) Create and activate a virtual environment:

On Windows:

python -m venv venv
venv\Scripts\activate
On macOS/Linux:

python3 -m venv venv
source venv/bin/activate
Install the required Python packages:

pip install django
Note: This project does not include a requirements.txt file. You may add one if you want to manage dependencies more easily.

Apply database migrations:

python manage.py migrate
Seed the database with initial quiz data:

python manage.py seed_quiz
Running the Development Server
Start the Django development server by running:

python manage.py runserver
The server will start at http://127.0.0.1:8000/.

Accessing the Application
Open your web browser and navigate to:

http://127.0.0.1:8000/
You can register a new user, login, and start taking quizzes.

Additional Notes
The project uses a SQLite database file named quiz_app.db.
Static files such as CSS are located in the static/ directory.
Templates for the web pages are located in the templates/ directory.
