from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(label="",
            widget=forms.TextInput(
                attrs={"class": "form-control rounder-form", 'autocomplete':'off'}
                )
            )

