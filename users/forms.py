from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms


class CreerUtilisateur(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']

class ModifierUtilisateur(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(max_length=60, required=False)
    message = forms.CharField(widget=forms.Textarea)
