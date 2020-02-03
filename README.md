# flask secret santa

This is a simple python bot to to draw names and send a text message to the participants.

### python code formartter

- [`black`](https://github.com/psf/black)
- [`flake8`](http://flake8.pycqa.org/en/latest/)

### libs

- config: [`dynaconf`](https://dynaconf.readthedocs.io/en/latest/)
- admin: [`flask_admin`](https://flask-admin.readthedocs.io/en/latest/)
- log: [`logging`](https://flask.palletsprojects.com/en/1.0.x/logging/)
- db: [`flask_sqlalchemy`](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) and [`flask_migrate`](https://flask-migrate.readthedocs.io/en/latest/)

## setup

### create and configure .env file

```
$ cp .env.sample .env
```

add the env vars:

```
FLASK_APP=secretsanta.app:create_app
SECRET_KEY="71b40786-c246-47c9-b3b1-cabe6917e0f6"
FLASK_ENV=development
```

### create and configure .secrets.toml

```
$ cp .secrets.toml.sample .secrets.toml
```

```
[default]
CSRF_SESSION_KEY = ""
JWT_SECRET_KEY = ""
TELEGRAM_BOT_TOKEN = ""
BOT_HOST = "https://"
```

### configure the .settings.toml

Open the .settings.toml file and check all variables. See if you want change any thing. I set the `SQLALCHEMY_DATABASE_URI` to connect with the mysql credentials that I defined in docker-compose file. If you change one of these files, remenber to change other.

## run

### docker-compose

You can run the app using the docker-compose file.

```
$  docker-compose up --build
```

To test, run `ngrok` to expose your local server:

```
$ ./ngrok http 5000
ngrok by @inconshreveable

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.3.35
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://732498a9.ngrok.io -> http://localhost:5000
Forwarding                    https://732498a9.ngrok.io -> http://localhost:5000
```

### flask run

#### virtualenv

```
# virtualenv
$ virtualenv -p python3 env
$ source env/bin/activate
# pyenv
$ pyenv virtualenv 3.7.4 secretsanta
$ pyenv activate secretsanta
```

#### install requirements

```
$ cd secretsanta
$ pip install -r requirements-dev.txt
```

_note_: `requirements-dev.txt` has all requirements packages to test, coverage and lint. If you don't want this packages, just run `pip install -r requirements.txt`.

#### migrate

```
$ flask db init
$ flask db migrate
$ flask db upgrade
```

#### run

```
$  flask run
```
