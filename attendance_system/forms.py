from django.core import validators
from django import forms
from .models import Person, City,Country

class FacultyRegisteration(forms.ModelForm):
    class Meta:
        model=Person
        fields='__all__'
        widgets= {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget=forms.HiddenInput()
        self.fields['is_pass_change'].widget=forms.HiddenInput()
        # self.fields['dept'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
class FacultyEditEmail(forms.ModelForm):
    class Meta:
        model=Person
        fields='__all__'
        widgets= {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
            # 'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget=forms.HiddenInput()
        self.fields['is_pass_change'].widget=forms.HiddenInput()
        self.fields['reg_id'].widget.attrs['readonly']=True

class FacultyEdit(forms.ModelForm):
    class Meta:
        model=Person
        fields='__all__'
        widgets= {
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget=forms.HiddenInput()
        self.fields['is_pass_change'].widget=forms.HiddenInput()
        self.fields['reg_id'].widget.attrs['readonly']=True
        self.fields['email'].widget.attrs['readonly']=True
        # self.fields['dept'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
