# Issue Tracker

## Clone the Project
```sh
$ git clone https://github.com/aarsh-sharma/Issue-Tracker
$ cd Issue-Tracker
```

## To Run the Project
Create a virtual environment to install dependencies in and activate it:


```sh
$ pip install virtualenv   # Ensure pip and python is installed on your system
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt    # Install all requirements
(env)$ python manage.py makemigrations    # Make Database Migrations
(env)$ python manage.py migrate           # Migrate Changes
(env)$ python manage.py runserver         # Run Local Server
```

## Instructions

- Make user to use any functionality
- You can create ticket and assign other users to it.
- Your tickets and tickets assigned to you will be displayed in your list.
- You can't access others' ticket.

### TODO

- [x] Make models
- [x] User Login & Auth
- [x] Make view for List
- [x] Make view for Ticket Detail
- [ ] Make a kanban board like view