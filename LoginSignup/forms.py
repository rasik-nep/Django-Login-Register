from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
    address = forms.CharField(max_length=255, required=True, help_text='Required. Enter your address.')

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "address", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # For signup, set the username as a combination of first_name and last_name
        user.username = f"{user.first_name} {user.last_name}"

        if commit:
            user.save()

            # Create a UserProfile instance and link it to the user
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address']
            )

        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)