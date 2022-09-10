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
  

## REST Endpoints

- `GET` -> `/tweets/` -> returns current users tweets (_auth required_)
- `POST` -> `/tweets/` -> create new tweet (_auth required_)
- `GET` -> `/tweets/<uuid>/` -> return tweet details
- `PUT` -> `/tweets/<uuid>/` -> make an edit to the tweet text (_author only_)
- `DELETE` -> `/tweets/<uuid>/` -> delete tweet (_author only_)
- `PUT` -> `/tweets/<uuid>/like/` -> increment tweet likes by 1 (_auth required_)


_View the users `urls.py` file for the user account endpoints._

## Coverage Report

```
Name                   Stmts   Miss  Cover
------------------------------------------
tweets/permissions.py       6      0   100%
tweets/serializers.py      17      0   100%
tweets/views.py            45      0   100%
users/managers.py         18      7    61%
users/serializers.py      23      0   100%
users/views.py            32      2    94%
------------------------------------------
TOTAL                    141      9    94%
----------------------------------------------------------------------
Ran 40 tests in 6.803s

OK
```

**Written by Jimawo Emmanuel**