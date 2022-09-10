# A simple social media application

This is a simple social media application REST API built using **Django and Django-REST-Framework (DRF)**. This API allows users to register for accounts, create tweets, and like others' tweets. Authentication is done using SimpleJWT. Testing is implemented with django-nose and coverage (see coverage report below).

**Project Goals:**

- User registration using unique username and a password
- User login (Including session maintenance using any means you’re comfortable with)
- Create, read, update, delete tweet (Twitter doesn’t support update, can you?)
- Unit/Integration tests for **all** basic methods and endpoints you’ve built so far (Basic & Extended Functionality)
- Like/unlike a tweet
- Retweet
- Threading

**To run app**
- cd speertweet_backend 
- python manage.py runserver
  
## REST Endpoints

- `GET` -> `/accounts/me/` -> returns current user (_auth required_)
- `POST` -> `/accounts/register/` -> register new user,
- `POST` -> `/accounts/login/` -> login user,
- `GET` -> `/accounts/<str:username>/` -> returns user details (_auth required_),

- `GET` -> `/tweets/` -> returns current users tweets (_auth required_)
- `POST` -> `/tweets/` -> create new tweet (_auth required_)
- `GET` -> `/tweets/<uuid>/` -> return tweet details
- `PUT` -> `/tweets/<uuid>/` -> make an edit to the tweet text (_author only_)
- `DELETE` -> `/tweets/<uuid>/` -> delete tweet (_author only_)
- `PUT` -> `/tweets/<uuid>/like/` -> increment tweet likes by 1 (_auth required_)


_View the users `urls.py` file for the user account endpoints._

## Coverage Report

**To run test**
- cd speertweet_backend 
- python manage.py test

```
Name                    Stmts   Miss  Cover
-------------------------------------------
tweets/permissions.py       6      0   100%
tweets/serializers.py       8      0   100%
tweets/views.py            38      0   100%
users/managers.py          18      7    61%
users/serializers.py       23      3    87%
users/views.py             26      2    92%
-------------------------------------------
TOTAL                     127     20    84%
----------------------------------------------------------------------
Ran 33 tests in 18.673s

OK
```

**Written by Jimawo Emmanuel**