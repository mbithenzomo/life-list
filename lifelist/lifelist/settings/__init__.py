import os

from django_envie.workroom import convertfiletovars

convertfiletovars()

# Ensure development settings are not used in testing and production:
if not os.getenv('Testing') and not os.getenv('Production'):
    from development import *

if os.getenv('Production') is not None:
    from production import *

if os.getenv('Testing') is not None:
    from testing import *
