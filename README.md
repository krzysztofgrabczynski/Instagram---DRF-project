
# <p align=center> <a name="top">Instagram---DRF-project </a></p>

This is the second version of the Instagram project on my github. If you want to check the previous version [click here.](https://github.com/krzysztofgrabczynski/Instagram---Django-project)

## Short overview
Version two of the Instagram project, fully utilizes Django Rest Framework to build a comprehensive RESTful API. The project was divided into apps for user, post, comment, and social actions, each handling specific functionalities. The project uses DRF's features like generic views, viewsets, and mixins which helped to create view classes. Additionally, it uses custom mixins and permissions to effectively extend view behaviors, along with serializers, routers, and more.

The project has been dockerized, uses PostgreSQL database, celery with redis for asynchronous tasks queue and linters such as Black, Flake8 and Mypy. The application has also been tested by Postman and unit tests (using pytest). 

This app was created for educational purposes.

If you want to check out my other projects [click here.](https://github.com/krzysztofgrabczynski)


## Description

In Instagram poject, users can create new accounts along with personalized profiles, log in securely (token authentication), and in case of a forgotten password, utilize the password reset functionality that sends a reset link to the user's registered email address. 

The project also empowers users to craft their own posts, explore the profiles of other users, follow their favorite accounts, and gain followers themselves. 

The platform encourages engagement by enabling users to like posts. Furthermore, users can easily manage their accounts, tweak profile settings, and edit/delete existing posts.

 ## Tools used in project:

<p align=center><a href="https://www.python.org"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/></a> 
<a href="https://www.djangoproject.com/"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="60" height="60"/> </a>
<a href="https://git-scm.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="git" width="60" height="60"/> </a> 
<a href="https://www.postgresql.org.pl/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/postgresql/postgresql-original-wordmark.svg" alt="psql" width="60" height="60"/> </a>
<a href="https://www.docker.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/docker/docker-original-wordmark.svg" alt="docker" width="60" height="60"/> </a>
<a href="https://redis.io//"> <img src="https://github.com/devicons/devicon/blob/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="60" height="60"/> </a>
<a href="https://python-poetry.org/"> <img src="https://github.com/python-poetry/website/blob/main/static/images/logo-origami.svg" alt="redis" width="60" height="60"/> </a></p>
<br> 

## Directory tree

```

├───core                        # Main direcory of the project with files such as 'settings.py', etc.
├───src                         # Directory with divided apps
│   ├───comment                 
│   ├───post
│   ├───social_actions
│   └───user
└───tests                       # Directory with unit tests. Divided per each apps and functionalities.
    ├───comment
    ├───post
    ├───social_actions
    └───user
│   .dockerignore
│   .gitignore
│   Dockerfile
│   README.md
│   manage.py
│   pytest.ini
│   requirements.txt
```
## Install for local use (using Docker)
- Clone the repository
- Create .env file and add requirement variables such as 'SECRET_KEY' or database parameters
- Build the Docker image using ``` docker-compose build ```
- Run containers using ``` docker-compose up ```
- Everything done! 

## Install for local use (using poetry)
- Clone the repository
- Create .env file and add requirement variables such as 'SECRET_KEY' or database parameters
- Enter the ``` poetry install ```
- Now enter the ``` poetry shell ``` to open virtualenv and start app with ``` python manage.py runserver ```
- Everything done! You can open Instagram app in your browser by ctrl + left click on http link in your console

For local use without Docker, you also need to configure Postgres and Celery with Redis.

[Go to top](#top) 
