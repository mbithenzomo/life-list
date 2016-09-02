[![CircleCI](https://circleci.com/gh/andela-mnzomo/life-list/tree/develop.svg?style=shield)](https://circleci.com/gh/andela-mnzomo/life-list/tree/develop)
[![Coverage Status](https://coveralls.io/repos/github/andela-mnzomo/life-list/badge.svg)](https://coveralls.io/github/andela-mnzomo/life-list)
[![Code Health](https://landscape.io/github/andela-mnzomo/life-list/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-mnzomo/life-list/develop)
![alt text](https://img.shields.io/badge/python-2.7-blue.svg)

# LifeList
![LifeList Logo](https://github.com/andela-mnzomo/life-list/blob/develop/lifelist/app/static/images/logo_blue_large.png)


According to the [Oxford Dictionary](http://www.oxforddictionaries.com/definition/english/bucket-list),
a *bucket list* is a *number of experiences or achievements that a person hopes
to have or accomplish during their lifetime*.

LifeList is a bucket list service built in Python/Django.

## Installation and Set Up
Prerequisites:
* [Python 2](https://www.python.org/download/releases/2.7.2/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

Clone the repo from GitHub:
```
git clone https://github.com/andela-mnzomo/life-list
```

Open the life-list directory:
```
cd life-list
```

Create a virtual environment for the project and activate it:
```
virtualenv lifelist
source lifelist/bin/activate
```

Install the required packages:
```
pip install -r requirements.txt
```

## Launching the Program
Run ```python lifelist/manage.py runserver``` to launch LifeList. You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API. You may also use [Curl](https://curl.haxx.se/), a command line tool. Precede the URL's below with `localhost:8000` to access the endpoints outlined.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
|  `/api/v1/auth/login/` | POST | User login | FALSE |
| `/api/v1/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/api/v1/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item | TRUE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |

## Web Application
LifeList also has a web application where users can register or login, and add bucket lists as well as items to their existing bucket lists. The application is live at [lifelist-app.herokuapp.com](http://lifelist-app.herokuapp.com/).

![Web App](https://github.com/andela-mnzomo/life-list/blob/develop/lifelist/app/static/images/screenshot.png)
* * *

## Testing
To test, run the following command: `python lifelist/manage.py test lifelist`.

## Built With...
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](http://www.django-rest-framework.org/)

## Credits and License

Copyright (c) 2016 [Mbithe Nzomo](https://github.com/andela-mnzomo)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
