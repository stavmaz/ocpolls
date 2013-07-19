from django import forms
from polls.models import Poll
from django.forms.widgets import Textarea


class CreatePollForm(forms.ModelForm):
    text = forms.CharField(widget=Textarea)

    class Meta:
        model = Poll
        fields = ()

