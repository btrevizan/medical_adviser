# Medical Advisor
Like a trip advisor for doctors and patients.

## Running on localhost

### First steps
You should have installed MySQL database. See `medical_advisor/settings.py` for database information.

To install the required packages, run:
```bash
$ sudo pip3 install -r requirements.txt
```

You should create a database called `medical_advisor`. Then run:
```bash
$ python3 manage.py migrate
```
This will make Django create a set of tables on your database. Don't worry, he will manage it.

### Starting the server
To start the server, run:
```bash
$ python3 manage.py runserver
```
You will see something like this
```bash
Performing system checks...

System check identified no issues (0 silenced).
<your date>
Django version 2.1.1, using settings 'medical_advisor.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

On your browser, enter: `http://127.0.0.1:8000/`

Done!
