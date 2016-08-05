import os

from django_envie.workroom import convertfiletovars

convertfiletovars()

# Ensure development settings are not used in testing and production:
if not os.getenv('Testing') and not os.getenv('Production'):
    from base import *

if os.getenv('Production') is not None:
    from production import *
