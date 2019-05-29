import django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reservation, Review


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["user","day", "time_slot", "num_people"]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('user','message', 'rating','number')


#Formulario para cambiar la informacion de perfil
class CommercialForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=128,required=False)
    #screen_name = forms.CharField(max_length=50, required=False)  # name that appears on screen (complementary username)
    birthday = forms.DateField(required=False)
    #password = forms.CharField(widget=forms.PasswordInput,required=False)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'birthday','password1', 'password2', )
        help_texts = {
            'username': None,
            #'password2': None,
        }

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ('username','password')
        help_texts = {
            'username': None,

        }