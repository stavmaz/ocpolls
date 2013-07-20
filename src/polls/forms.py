from django import forms


class CreatePollForm(forms.Form):
    text = forms.TextInput('Proposals', widget=forms.Textarea)
