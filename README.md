[![DOI](https://zenodo.org/badge/58523978.svg)](https://zenodo.org/badge/latestdoi/58523978)

# dig_ed_cat
## About
A web application to browse, analyze and curate a catalogue of digital editions (https://dig-ed-cat.acdh.oeaw.ac.at/). 
The catalogue's data was gathered and curated by *Greta Franzini*. See https://github.com/gfranzini/digEds_cat

## Install
The application was build with Python 3.4. Be aware that it uses a modularized settings configuration (e.g. to keep sensitive information out of GitHub). Therefore you'll have to append the default django manage.py commands with a **settings-parameter** like `--settings=digital_editions.settings.dev` 

1. clone the repo
2. create a virtual environment and run install the required packages `pip install > requirements`
3. makemigrations and migrate `python manage.py makemigrations --settings=digital_editions.settings.dev` and `python manage.py migrate --settings=digital_editions.settings.dev`
4. start the dev-server `python manage.py runserver --settings=digital_editions.settings.dev`
5. browse to http://127.0.0.1:8000/

## Upload the data
To fetch the last version of the catalogue data, 

1. you have to create a (super)user account `python manage.py createsuperuser--settings=digital_editions.settings.dev`
2. browse to http://127.0.0.1:8000/
3. log in (icon in the top right corner)
4. then you'll see a 'Curate the Data' -> 'Sync with GitHub' nav bar entry, 
5. click on it and then on the button which says 'click me to snyc'.
test
