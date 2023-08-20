
# <p align=center> <a name="top">Instagram---DRF-project </a></p>

This is the second version of the Instagram project on my github. If you want to check the previous version [click here.](https://github.com/krzysztofgrabczynski/Instagram---Django-project)

## Short overview
Version two of the Instagram project, fully utilizes Django Rest Framework to build a comprehensive RESTful API. The project was divided into apps for user, post, comment, and social actions, each handling specific functionalities. The project uses DRF's features like generic views, viewsets, and mixins which helped to create view classes. Additionally, it uses custom mixins and permissions to effectively extend view behaviors, along with serializers, routers, and more.

The project has been dockerized, uses PostgreSQL database and linters such as Black, Flake8 and Mypy. The application has also been tested by Postman and unit tests (using pytest).

This app was created for educational purposes.

If you want to check out my other projects [click here.](https://github.com/krzysztofgrabczynski)

## Description

In Instagram poject, users can create new accounts along with personalized profiles, log in securely (token authentication), and in case of a forgotten password, utilize the password reset functionality that sends a reset link to the user's registered email address. 

The project also empowers users to craft their own posts, explore the profiles of other users, follow their favorite accounts, and gain followers themselves. 

The platform encourages engagement by enabling users to like posts. Furthermore, users can easily manage their accounts, tweak profile settings, and edit/delete existing posts.

## Install for local use 
- Copy the repository
- Create virtual environment using ``` python -m venv venv ``` in project directory
- Use ``` . venv/Scripts/activate ``` to activate the virtual environment
- Install required packages by ``` pip install -r requirements.txt ```
- Enter the ``` python manage.py migrate --run-syncdb ``` to update migrations
- Now, you can run the application with this: ``` python manage.py runserver ```
- Everything done! You can open Instagram app in your browser by ctrl + left click on http link in your console

## Directory tree

```

├───core                        # Main direcory of the project with files such as 'settings.py', etc.
├───src                         # Directory with divided apps
│   ├───comment                 
│   ├───post
│   ├───social_actions
│   └───user
└───tests                       # Directory with unit tests. Divided per all apps and functionalities.
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

[Go to top](#top) 
