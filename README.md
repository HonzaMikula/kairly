# kairly

> New way how we consume and produce news

http://kairly.honzamikula.cz/

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

Install pipenv, then

```
pipenv install
```

Create your settings with database config. Then setup env variable.
```
echo "DJANGO_SETTINGS_MODULE=kairly.settings_myconf" > .env
```

Create database and sync tables.
```
pipenv run ./manage.py migrate
```

## Run Python Devserver

```
pipenv run ./manage.py runserver
```
