import unittest

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver

from accounts.models import UserProfile
from deals.models import Advertiser, Category, Deal
from merchant.models import Merchant
