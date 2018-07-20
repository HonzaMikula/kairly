# kairly

> New way how we consume and produce news

https://kairly.com/

## Build Vue Prototype

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# serve with hot reload at localhost:8080 and connect to local Python server
npm run local

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

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

First run Webpack on client

```
webpack --watch --config build/webpack.prod.conf.js
```

```
pipenv run ./manage.py runserver

```

## Rosti

Run command, eg.
```
DJANGO_SETTINGS_MODULE=kairly.settings_prod ./manage.py importrss --provider=janmikula
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
