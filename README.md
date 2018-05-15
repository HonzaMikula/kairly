# kairly

> New way how we consume and produce news

http://kairly.com/

## Build Vue Prototype

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

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

h1:
  exclude: 1
```

### Changing order of tags
```
p

img:fist-child
    odering: 1```

or

```
p

img:fist-child
  move-after: p:first-child\
```

### Renaming tags
```
div#main-content
  h3
    as: p
```
