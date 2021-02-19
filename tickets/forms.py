from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Ticket


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'state', 'severity', 'issue_type', 'assigned_to', 'details']


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['state', 'severity', 'issue_type', 'details', 'assigned_to']


class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, required=False, label='')

    def clean_body(self):
        value = self.cleaned_data.get('body', '').strip()
        if value == '':
            raise forms.ValidationError("Empty comment.")
        return value
