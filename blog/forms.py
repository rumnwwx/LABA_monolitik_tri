from django import forms
from django.core.exceptions import ValidationError
from .models import User, Post, Comment


class UserCreatingForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    avatar = forms.ImageField(widget=forms.FileInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такое имя пользователя занято.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такой адрес электронной почты занят.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", 'email', 'avatar')


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите текст поста'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})
        }