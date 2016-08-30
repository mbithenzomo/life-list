import os

from django_envie.workroom import convertfiletovars

convertfiletovars()

# Ensure development settings are not used in testing and production:
if os.getenv('HEROKU') is not None:
    from production import *
elif os.getenv('CI') is not None:
    from testing import *
else:
    from development import *
