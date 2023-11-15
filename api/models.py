from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None or password is None:
            raise TypeError('Users must have email address and password')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if email is None or password is None:
            raise TypeError('Users must have email address and password')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class BookstoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, null=False, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Book(TimestampModel):
    title = models.CharField(max_length=128, null=False)
    author = models.CharField(max_length=128, null=False)
    publish_date = models.DateField(null=True)
    ISBN = models.CharField(max_length=50, null=False, unique=True)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.title


class BookCover(TimestampModel):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    image = models.ImageField(null=False, upload_to='media/')
