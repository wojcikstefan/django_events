from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from models import Event, Ticket

class LoginForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput,
                               label=_('Password'))
    
class RegisterForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput,
                               label=_('Password'))
    re_password = forms.CharField(max_length=30, widget=forms.PasswordInput,
                               label=_('Retype password'))
    
    def clean(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError(_('User with given e-mail already exists'))
        passwd1 = cd.get('password')
        passwd2 = cd.get('re_password')
        if passwd1 != passwd2:
            raise forms.ValidationError(_('Passwords did not match'))
        return cd
    
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by',)
        
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('event',)
        