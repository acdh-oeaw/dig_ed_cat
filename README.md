# dig_ed_cat
## About
A web application to browse, analyze and curate a catalogue of digital editions.
The catalogue's data was gathered and curated by *Greta Franzini*. See https://github.com/gfranzini/digEds_cat

## Install
The application was build with Python 3.4.

1. clone the repo
2. create a virtual environment and run install the required packages `pip install > requirements`
3. makemigrations and migrate `python manage.py makemigrations`and `python manage.py migrate`
4. start the dev-server `python manage.py runserver`
5. browse to http://127.0.0.1:8000/

## Upload the data
To fetch the last version of the catalogue data, you have to execute the ipython script `import_editions.ipynb`.

1. Start a new iypthon session `python manage.py shell_plus --notebook`.
2. Open `import_editions.ipynb`.
3. Execute the script cell by cell. 
