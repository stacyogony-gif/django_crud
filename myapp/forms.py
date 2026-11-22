from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields =('name','photo','email','password','mobile_number','date_of_birth')
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Leave blank to keep the current password.'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password and self.instance.pk:
            return self.instance.password
        return password
