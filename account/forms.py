from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Profile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    The default 

    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'id': 'createPassword'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password Again', 'id': 'confirmPassword'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control disabled',
                'placeholder': 'Enter Email',
                'id': 'email',
                'inputmode': 'email',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email Address already taken!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Password fields do not match. Recheck...")
        return password2

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'professional_prefix', 'membership_level']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter Fullname',
                'id': 'name',
            }),
            'professional_prefix': forms.TextInput(attrs={
                'placeholder': 'E.g: Dr, Prof, etc ',
                'id': 'profession',
            }),
            'membership_level': forms.Select(attrs={
                'id': 'membership-level',
            }),
        }
    
    
    '''
    def clean(self):
        cleaned_data = super().clean()
        professional_prefix = cleaned_data.get('professional_prefix')
        if len(professional_prefix) > 20:
            raise forms.ValidationError("Please enter the shorter form of your professional prefix")
        if not professional_prefix:
            raise forms.ValidationError("Professional prefix cannot be empty")
        return cleaned_data
    '''
    
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'gender', 'country', 'phone_number', 'picture']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'id': 'fullname',
            }),
            'gender': forms.Select(attrs={
                'id': 'gender',
            }),
            'age_range': forms.Select(attrs={
                'id': 'age-range',
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'phone-number',
            }),
            'country': forms.TextInput(attrs={
                'id': 'country',
            }),
            'picture': forms.FileInput(attrs={
                'id': 'pic-upload-input',
                'hidden': 'hidden',
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email',]

        widgets = {
            'email': forms.EmailInput(attrs={
                'id': 'email',
            }),
        }
