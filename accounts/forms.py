from django import forms
from .models import Account

class RegistrationForms(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Enter the password'
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Enter the password',
        }
    ))

    class Meta:

        model = Account
        fields = [
            'first_name', 'last_name', 'phone_number',
            'email',
            'password'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForms, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'

        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'

        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your Phone Number'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):

        cleaned_data = super(RegistrationForms, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password didnt match'
            )