# from django import forms
from django import forms
from .models import CustomUser

# ---------------- Registration Form ----------------
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'api_key', 'secret_key', 'client_code', 'angelone_password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your AngelOne API key'}),
            'secret_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your AngelOne Secret key'}),
            'client_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your AngelOne Client Code'}),
            'angelone_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your AngelOne Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set hashed password
        user.set_password(self.cleaned_data["password1"])

        # Encrypt AngelOne credentials
        user.set_encrypted_field("api_key", self.cleaned_data.get("api_key"))
        user.set_encrypted_field("secret_key", self.cleaned_data.get("secret_key"))
        user.set_encrypted_field("angelone_password", self.cleaned_data.get("angelone_password"))

        if commit:
            user.save()
        return user


# ---------------- Login Form ----------------
class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

