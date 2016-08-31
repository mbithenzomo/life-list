from api.models import Bucketlist, Item
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class LoginForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ('username', 'password')


class BucketlistForm(forms.ModelForm):

    class Meta:

        model = Bucketlist
        fields = ('title', 'description', 'image')


class ItemForm(forms.ModelForm):

    class Meta:

        model = Item
        fields = ('title', 'description', 'is_done')
