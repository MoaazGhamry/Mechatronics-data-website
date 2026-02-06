from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Level, Subject, SubjectResource, StudentProfile

class StudentSignUpForm(UserCreationForm):
    level = forms.ModelChoiceField(
        queryset=Level.objects.all().order_by('level_id'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "This username is already taken. Please choose another.",
                code='username_taken',
            )
        return username

class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="PASSWORD", 
        widget=forms.PasswordInput(attrs={
            'class': 'form-input', 
            'placeholder': '••••••••', 
            'autocomplete': 'new-password'
        }),
        required=True,
        min_length=1,  # Allow any length
        help_text="Enter any password (no complexity requirements)"
    )
    level = forms.ModelChoiceField(
        label="LEVEL",
        queryset=Level.objects.all().order_by('level_id'),
        required=False,
        empty_label="No level",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    account_type = forms.ChoiceField(
        label="ACCOUNT TYPE",
        choices=[('student', 'Student'), ('admin', 'Admin')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
        }
        labels = {
            'username': 'USERNAME',
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
        }

    def clean_password(self):
        """Skip Django's default password validators"""
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        # Role logic
        acc_type = self.cleaned_data.get('account_type')
        if acc_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        
        if commit:
            user.save()
            # Link level to StudentProfile (created by signals)
            level = self.cleaned_data.get('level')
            profile = user.profile
            if level:
                profile.level = level
            
            # Store plain password
            profile.plain_password = self.cleaned_data.get('password')
            profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['gpa', 'profile_picture_url']
        widgets = {
            'gpa': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': '0.0', 'max': '4.0'}),
            'profile_picture_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
        }
    
    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa < 0 or gpa > 4.0:
            raise ValidationError("GPA must be between 0.0 and 4.0.")
        return gpa

class PDFUploadForm(forms.ModelForm):
    level = forms.ModelChoiceField(
        queryset=Level.objects.all().order_by('level_id'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    semester = forms.ChoiceField(
        choices=[(1, 'Semester 1'), (2, 'Semester 2')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = SubjectResource
        fields = ['preview_url', 'download_url', 'category', 'subject']
        widgets = {
            'preview_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Google Drive Embed URL'}),
            'download_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Google Drive Download URL'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].queryset = Level.objects.all().order_by('level_id')
        self.fields['subject'].queryset = Subject.objects.none()

        if 'level' in self.data and 'semester' in self.data:
            try:
                level_id = self.data.get('level')
                semester = self.data.get('semester')
                self.fields['subject'].queryset = Subject.objects.filter(level_id=level_id, semester=semester).order_by('name')
            except (ValueError, TypeError):
                pass
