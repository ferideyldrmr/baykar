from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from core.models import RentalRecord, Rental


class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}), )
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class DonationForm(forms.Form):
    amount = forms.DecimalField(label='Amount', decimal_places=2)
    email = forms.EmailField(label='Email')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class RentalRecordForm(forms.ModelForm):
    class Meta:
        model = RentalRecord
        fields = ['user', 'uav', 'status', 'return_date']


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        exclude = ['rental_date']


class UAVForm:
    pass


class Lease:
    def __init__(self, start_date, end_date, renter):
        self.start_date = start_date
        self.end_date = end_date
        self.renter = renter

    def __str__(self):
        return f"Lease: {self.start_date} to {self.end_date} - Renter: {self.renter}"


class LeaseForm:
    pass