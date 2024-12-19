from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=100, verbose_name='Имя пользователя', unique=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название поста')
    content = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Дата и время')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"Post by {self.author} on {self.published_at.strftime('%Y-%m-%d %H:%M')}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"