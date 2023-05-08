from django import forms
from .models import UrlCheck


class UrlCheckForm(forms.ModelForm):
    class Meta:
        model = UrlCheck
        fields = ['url']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].label = 'Please enter URI to test'
        self.fields['url'].widget.attrs.update({'placeholder': 'https://wttr.in/876'})
        self.fields['url'].widget.attrs.update({'autocomplete': 'off'})

        # self.fields['submit'].widget.attrs.update({'class': 'btn btn-primary', 'id': 'submit-id'})
        # self.fields['submit'].label = 'Test URI'