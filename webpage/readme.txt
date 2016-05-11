1. create a new django project
2. copy the webpage-directory into the new projects root directory
3. cd to webpage/config
4. copy and paste the requirements.txt into the new projects root directory
5. create a virtual environment
6. activate it and run pip install -r requirements.txt (tested on windows 8.1, python 3.4)
7. adapt the projects settings.py und urls.py according to the code snippets in webpage/config
8. run migrations
9. fire the testserver

add other 'django-generic-apps'
be aware that: 'labels' depends on 'webpage' and 'places' depends on 'webpage' and 'labels'
1. copy them in the projects root directory
2. set the projects settings and urls
3. run migrations
4. fire the testserver
