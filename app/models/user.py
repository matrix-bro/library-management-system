from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserAccountManager(BaseUserManager):

    def create_user(self, name, email, membership_date, password=None):
        if not email:
            raise ValueError('Email field is required')
        
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(name=name, email=email, membership_date=membership_date)

        user.set_password(password)

        user.save(using=self._db)

        return user
    
    def create_superuser(self, name, email, membership_date, password=None):

        user = self.create_user(name, email, membership_date, password=password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)    
    email = models.EmailField(max_length=200, unique=True)
    membership_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'membership_date']

    def __str__(self):
        return self.email
