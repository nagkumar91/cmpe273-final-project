Set Up and running your code:

1. Create a virtualenv. (http://docs.python-guide.org/en/latest/dev/virtualenvs/)

2. Activate the virtualenv. 

```
source <path_to_venv>/bin/activate
```

3. Install all the requirements.

```
cd <path_of_project>
pip install -r requirements/local.txt
```


4. Create a settings file 

```
cp twitter_analytics/settings/local.py twitter_analytics/settings/<your_name>.py
```


5. Edit your settings file to insert correct db credentials (https://docs.djangoproject.com/en/1.6/ref/settings/#databases)

6. Create the database (ignore on sqllite)

7. Export your settings file to the env

```
export DJANGO_SETTINGS_MODULE=twitter_analytics.settings.<your_name>.py
```


8. Sync db

```
python manage.py syncdb
```


9. Run migrations

```
python manage.py migrate
```


10. Create admin (if you do not have one)

```
python manage.py createsuperuser
```


11. Run server!

```
python manage.py runserver 0.0.0.0:8081
```
