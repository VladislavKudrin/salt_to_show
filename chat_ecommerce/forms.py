from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(label="",
            widget=forms.Textarea(
                attrs={"class": "form-control rounder-form", 'autocomplete':'off', 'rows': '1', 'cols':'1'}
                )
            )

