import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from auths.models import User, PhoneNumber, UserAddress, get_language_choices, get_gender_choices
from captcha.fields import CaptchaField  # Import captcha field
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import password_validators_help_texts

# List of common disposable email domains
DISPOSABLE_EMAIL_DOMAINS = [
    "tempmail.com", "10minutemail.com", "mailinator.com", "guerrillamail.com",
    "dispostable.com", "yopmail.com", "fakeinbox.com"
]


def normalize_email(value):
    """Remove aliasing (sub-addressing) from emails."""
    local_part, domain = value.split("@")
    local_part = re.sub(r"\+.*", "", local_part)  # Remove anything after "+"
    return f"{local_part}@{domain}"


def validate_email(value):
    """Check if the email belongs to a disposable provider and remove aliasing."""
    normalized_email = normalize_email(value)
    domain = normalized_email.split("@")[-1]

    if domain in DISPOSABLE_EMAIL_DOMAINS:
        raise forms.ValidationError("Disposable email addresses are not allowed.")

    return normalized_email  # Return the cleaned email


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text="Enter a valid email address.",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                message="Enter a valid email address."
            )
        ],
    )

    def clean_email(self):
        """Override the clean method to remove aliasing before saving."""
        email = self.cleaned_data.get("email")
        email = validate_email(email)  # Normalize and validate
        return email  # Save the cleaned email

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=" ".join(password_validators_help_texts()),  # Dynamically generate help text
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Enter the same password as above, for verification.",
    )
    gender = forms.ChoiceField(
        choices=[("", "Select Gender")] + get_gender_choices(),  # Add a blank choice
        required=False,  # Make it optional
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Select your gender (optional)."
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Enter date of birth."
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        help_text="Upload a profile picture."
    )

    captcha = CaptchaField(
        help_text="Enter the security code."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "date_of_birth",
            "gender",
            "profile_picture",
            "captcha"
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
