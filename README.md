# kairly

> New way how we consume and produce news

https://kairly.com/

## Build Vue client

``` bash
# install utilities required for i18n
apt install gettext python3-pip
python3 -m pip install polib

# install dependencies
npm install

# compile messages
npm run compilemessages

# serve with hot reload at localhost:3000
npm run dev

# serve with hot reload at localhost:3000 and connect to local Python server
npm run local
```

## Setup Python Environment

Install [pipenv](https://docs.pipenv.org/), then

```
pipenv install
```

Create your settings with database config. Then setup env variable
(with your own settings file, you can use settings_farin.py as template)
```
echo "DJANGO_SETTINGS_MODULE=kairly.settings_myconf" > .env
```

Create database and sync tables.
```
pipenv run ./manage.py migrate
```

Create your admin account
```
pipenv run ./manage.py createsuperuser
```

## Run Dev server

```
pipenv run ./manage.py runserver

```

## I18n

``` bash
# refresh .po files
npm run compilemessages

# edit translation strings
poedit locales/cs.po
# or use poedit windows port

# compile .po files to JSONs used by app
npm run makemessages
```

## Rosti

Run command, eg.
```
DJANGO_SETTINGS_MODULE=kairly.settings_prod ./manage.py importrss --provider=
```

## Deployment

Move `production` tag to trigger Circle CI deployment task.
```
git tag -f production && git push -f --tags
```

## Import RSS
Fetch & import all
```
pipenv run ./manage.py importrss --force
```

Fetch & import specific source
```
pipenv run ./manage.py importrss --provider=idnescz
```

## Import RSS Rules

### Exclude tag
```
*

h1
  tag: none
```

### Changing order of tags

```
p

img[0]
  move-after: p[1]
```

### Renaming tags
```
div#main-content
  h1
    tag: h2
```

## Users before migration

(Emails should be filled)

alenamarasova	 	                        Alena	Mařesová
farin	                  	              Roman	Krejčík
honzamikula	   	                        Jan	Mikula
janhavel	                            	Jan	Havel
jirikocib	                             	Jiří	Kočíb
marekcerovsky	                         	Marek	Čeřovský
martinmikula                            Martin Mikula
oskarhollmann	 	                        Oskar	Hollmann
qa@onboarding	 	                        QA	Kairly
romanriha	 	                            Roman	Říha
veronikasafarikova	 	                  Veronika Safaříková
veronikavamberova	 	                    Veronika	Vamberova
zbynekhujer                             Zbyněk Hujer
