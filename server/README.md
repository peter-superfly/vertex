# Backend

The Backend Service is responsible for the apis.

### Purpose
*  The Backend service manage to all backend tasks.

### Generate SSH key
* Run `$ ssh-keygen -t rsa -C "your_email@example.com"`
* Run `$ cat ~/.ssh/id_rsa.pub` and copy ssh key
* Add key in user profile of online code repository [Gitlab, Github or Bitbucket]


### Steps to install and run backend on your local machine
* Run `$ pip install virtualenv` command to install virtual environment
* Run `$ virtualenv env -p python3.7` command to Create Virtual environment
* Run `$ source env/bin/activate` command to activate virtual environment
* Run `$ git clone git@github.com:skyspace-live/server.git` command for cloning the project
* Run `$ cd server/server` command for jump into the project directory
* Run `$ pip install -r requirements.txt` command to Install project requirement file
* Run `$ export SECRET_KEY='some_long_random_string_goes_here'` to configure the secret key
* Run `$ python manage.py migrate` command to apply migrations on your local machine
* Run `$ python manage.py runserver` command to run project on your local machine
