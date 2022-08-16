
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your CustomManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email,first_name,last_name,birthday,gender,phone,usertype, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            first_name = first_name,
            last_name= last_name,
            birthday = birthday,
            gender = gender,
            usertype=usertype,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email,first_name,last_name,birthday,gender,phone,usertype, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, first_name,last_name,birthday,gender,phone,usertype, password, **extra_fields)

    def create_superuser(self, email,first_name,last_name,birthday,gender,phone,usertype, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        
        return self._create_user(email,first_name,last_name,birthday,gender,phone,usertype, password, **extra_fields)

# Create your models here.
class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255)
    username = None
    birthday = models.DateField()
    usertype = models.CharField(max_length=10,default='user')
    gender = models.CharField(max_length=12)
    phone = models.CharField(max_length=10,unique=True)
    
    def __str__(self):
        return self.email
    
    object = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','birthday','usertype','gender','phone']
    
    class meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
