from django.forms import ModelForm, Select,EmailInput
from myapp2.models import Example


class ExampleForm(ModelForm):
    template_name = 'myapp2/form_template.html'
    class Meta:
        model = Example
        fields=['name','surname','email','text','lavoro']
        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'Email',
                'aria-label': 'Email',
                'class': 'form-control'
            }),
            'lavoro': Select(attrs={
                'class': 'form-select',
                'aria-label': 'Seleziona il lavoro',
                'placeholder': "Seleziona il lavoro",
                })
            }