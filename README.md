# kairly

> New way how we consume and produce news

https://kairly.com/

## Build Vue client

``` bash
# install utilities required for i18n
apt install gettext python3-pip default-libmysqlclient-dev
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

Project requires Python 3.6+
Virtualenvwrapper is not necessary, but it is recommended. http://virtualenvwrapper.readthedocs.io/en/latest/

```
pip install virtualenvwrapper
```

Create virtual env for the project (isolated python environment)

```
mkvirtualenv --python=`which python3` kairly
````

Create your settings with database config (in /kairly-server/kairly)
(with your own settings file, you can use settings_farin.py as template)

Edit virtual env postactivate hook
```
nano ~/.virtualenvs/kairly/bin/postactivate
```

Let DJANGO_SETTINGS_MODULE point to your settings python file.
Eg. content of my postactive script
```
#!/bin/bash
# This hook is sourced after this virtualenv is activated.

export DJANGO_SETTINGS_MODULE=kairly.settings_farin
```

Deactivate and activate virtual env to trigger hook
```
deactivate
workon kairly
```

Install dependencies (run from kairly-server folder)
```
pip install -r requirements.txt
```

## Run Dev server

With enabled virtual env (`workon kairly`), run from kairly-sarver folder

Sync tables if new migrations exists
```
./manage.py migrate
```

```
./manage.py runserver

```

## I18n

``` bash
# refresh .po files
npm run makemessages

# edit translation strings
poedit locales/cs.po
# or use poedit windows port

# compile .po files to JSONs used by app
npm run compilemessages
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

### Attribute manipulations
```
img
  [src]: force-https
  [srcset]: none
  [sizes]: none
```

### Rename Attribute
```
img
  [data-orig-file]: rename src
```

## Selection with XPath

Sometimes elements can't be selected by CSS. XPath is more strong
and may be helpful. Eg. selection by text content

XPath rules can't be nested.
```
@xpath //*[contains(text(), "twitter-follow")]
  tag: none
```


## Channel directives

#### skip domain

Don't import posts hosted on given domain.
```
skip domain video.aktualne.cz
```

#### replace title

Use regular expression to modify post's title.
```
replace title '^\[článek\]\s*' ''
replace title '^\[aktualita\]\s*' ''
```

Use regular expression to modify perex/content.
```
replace document 'koleje' 'poleje'
```

## Management commands

### addfreecredits

Add free credits to user(s)

`./manage.py addfreecredits farin janmikuka --amount 100`

Remove credits from users

`./manage.py addfreecredits badboy --amount="-250"`

### costs

Show articles costs for author(s) and month

`./manage.py costs --month 12/2018 a2larm mariankechlibar`

### payauthors

Divide accumulated credits from author Subscriptions to user.
Invoked by cron at the end of each month.

### payeditors

Divide accumulated credits from newspaper Subscriptions to editor and authors.
Invoked by cron at the end of each month.

Can by run manually to see how will be credits distributed for current month.
`./manage.py payeditors --month 01/2019 --dry-run`
