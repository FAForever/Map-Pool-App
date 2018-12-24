# FAF Map Pool App

##### **Currently hosted at - https://fluffypoolapp.herokuapp.com/**
##### Initial load could be very slow, this is a limitation of Heroku free hosting

This is web app that allows for auto-generation of ladder/tournament map pools and any other arbitrary customized map selection. It is currently used by the ladder team of https://www.faforever.com/ to generate ladder pools.
Maps are fetched from the [ladder pool](https://goo.gl/wBqxQu) sheet where they review maps. (a cut version for the sake of sanity of ladder team)


:ok_hand: **Doesn't work in IE** :ok_hand:


Project uses Django with Django-Rest-Framework for back-end and React for front-end.

You will need python 3.6+, pip, pipenv and npm/yarn (pip 18.0 might throw exceptions) and node 8+

### Installing packages:

    -pipenv install
    -npm install

### Local Development:

Run over MapPoolApp/settings.py and change allowed hosts, add secret key to .env, change debug mode and whatever you need.
We use pipenv for virtual environment so just assume that you need to `pipenv shell` before running any python commands. `python manage.py loaddata djangoDump.json` to populate a db from maps fixture. It's real map data pulled from the ladder team sheet. If you have access to it or have created your own sheet you can use the `fetchMapsIntoJson` method from mappool/extra_logic/maps to get an updated json.


#### Production-like environment
###### Using Heroku:

    -npm build
    -heroku local -f Procfile.windows / heroku local Procfile

Project is configured for heroku deployment, if you have heroku CLI you can use `heroku local -f Procfile.windows` / `heroku local Procfile` to fire the commands in Procfile to launch the most close-to-production server available.

###### Without Heroku:

    -npm build
    -pipenv shell
    -python manage.py runserver

This will launch a django dev server. Basically the same as heroku method, just skipping some overhead that's useful if you are planning to deploy to heroku. Both of these methods are single-server, they serve static files from build or staticfiles folder in the root of this project depending if you run `python manage.py collectstatic`. To see any change to them you will have to build again.

#### Development environment
###### Two Development Servers:

    -pipenv shell
    -python manage.py runserver
    -npm start

You launch 2 dev servers for front-end and back-end separately in which case you don't need to build every time. They will use different ports so make sure to uncomment CORS_ORIGIN_ALLOW_ALL and cors middleware+app in MapPoolApp/settings.py for api fetching from local db.
