# Task List App

This is a simple list app to easily manage personal tasks.

## Content

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contact](#contact)

## Overview

- Tasks have a name, a content and a done property to set the finished or pending.
- You can switch between seeing all tasks and just the pending ones.
- Every time a task is updated(changed its name or content) is moved to the top to highlight importance.

## Installation

Step-by-step instructions, it is assumed that, python, pipenv, pyenv, node and docker are installd.
Otherwise refer to offical documentation, or contact me, I'll be willing to assist.

1. Clone the repository:
   ```bash
   git clone https://github.com/johan8863/task_list_app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd task_list_app
   ```
   In there you'll find two folder each for backend and frontend projects with those names. Lets install backend first.

3. Installing backend dependencies:
    ```bash
    cd backend
    ```
    - First install and run docker database containers, before running docker commands create a .env file and place in it the required variables in the docker-compose.yml file.
   ```bash
   docker compose up -d
   ```
   - Create virtual environment for python backend.
   ```bash
   pipenv shell
   ```
   - Install python requirements. Here also read the project/settings/base.py to create the required variables in the .env file mentioned above.
   ```bash
   pipenv install --ignore-pipfile
   ```
   The --ignore-pipfile argument is used to install the exact versions of frameworks and libraries of the project, to intall the latest non versioned ones in the Pipfile, that argument can be skipped.

   - Point a browser to http://localhost:8088/, enter with the server created in the docker-compose.yml, root user and the password provided in the .env password variable. Once in, create a database named tasks_list_prod.

   - Run the development server with:

   ```bash
   python manage.py runserver

   ```

   - Fronted dependencies
   ```cd ../frontend``` from the backend directory or just ```cd frontend``` from the root directory of the git downloaded project.

   - Install node dependencies:
   ```bash
   npm install
   ```

   - Run the development server:

   ```bash
   npm run dev
   ```

   Point a browser at http://localhost:5173/ and your app is ready to start receiveng tasks.

## Usage

The app has a top form in which you can insert tasks. once you type the name and the content of an app you can either click on the Add button or press enter, if name or content are omitted the app will complain about required inputs. Once you see the asks you added, you can update(modify) them by clicking in the update button, if a task is created or updated as done, won't be visible if the ```Show done``` checkbox isn't checked, that way, the user can focus mainly on pending tasks. That's it! 

## Testing

This project only has backend tests so far, therefore, to run the test, change to the backend directory and run ```coverage run manage.py test``` so that the ```coverage``` library starts meeting the project tests. Afterwards you can run ```coverage report``` to see the code coverage the project has.


## Contact

Johan Travieso Castro - [jtravieso8863@gmail.com](mailto:jtravieso8863@gmail.com)

Project Link: [https://github.com/johan8863/task_list_app](https://github.com/johan8863/task_list_app)
