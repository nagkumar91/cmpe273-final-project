Set Up and running your code:

* Create a virtualenv. (http://docs.python-guide.org/en/latest/dev/virtualenvs/)

* Activate the virtualenv. 

```
source <path_to_venv>/bin/activate
```

* Install all the requirements.
```
cd <path_of_project>
pip install -r requirements.txt
```

* Create a settings file 
```
cp twitter_analytics/settings/local.py twitter_analytics/settings/<your_name>.py
```

* Edit your settings file to insert correct db credentials (https://docs.djangoproject.com/en/1.8/ref/settings/#databases)

* Create the database (ignore on sqllite)

* Export your settings file to the env

```
export DJANGO_SETTINGS_MODULE=twitter_analytics.settings.<your_name>
```


* Sync db

```
python manage.py syncdb
```


* Run migrations

```
python manage.py migrate
```


* Create admin (if you do not have one)

```
python manage.py createsuperuser
```


*  Run server!

```
python manage.py runserver 0.0.0.0:8081
```


Deployment Instructions:
ssh to server
create user
add user to sudo (gpasswd -a user sudo)
create ssh pub key
add pub key to github's deployment keys
install db (postgresql)
install mod_wsgi
syncdb