# Test Task

Before starting, you must check for the existence of a virtual environment or create it if necessary.
If you are use Linux then you need write `python` or `python3` before commands listed below
In the directory with `requirements.txt` need running
``` 
pip install -r requirements.txt
```

In the directory Threads, where is `manage.py` need running
```
manage.py makemigrations
manage.py migrate
manage.py loaddata db.json
manage.py runserver
```
