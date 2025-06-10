from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django import forms
from .models import Profile


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required 150 characters or less. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small">Your password must contain at least 8 characters.Your password can\'t be entirely numeric.</ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UpdateUserForm(UserChangeForm):
	password=None
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required 150 characters or less. Letters, digits and @/./+/-/_ only.</small></span>'

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return new_password2

class UserInfoForm(forms.ModelForm):
    phone=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),required=False)
    address1=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required=False)
    address2=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}),required=False)

    city=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),required=False)
    state=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),required=False)
    zipcode=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}),required=False)
    country=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),required=False)		
    class Meta:
        model=Profile
        fields=('phone','address1','address2','city','state','zipcode','country')
