import os

from django_envie.workroom import convertfiletovars

convertfiletovars()

# Ensure development settings are not used in testing and production:
if os.getenv('Production') is not None:
    from production import *
elif os.getenv('Testing') is not None:
    from testing import *
else:
    from development import *
