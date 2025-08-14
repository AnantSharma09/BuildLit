from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
  def create_user(self,email,username,password=None,**extra_fields):
    if not email:
      raise ValueError("The Email field must be set")
    email = self.normalize_email(email)
    user = self.model(email=email,username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  def create_superuser(self, email, username="admin", password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self.create_user(email=email, username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=30, unique=True, null=True, blank=True)
  first_name=models.CharField(max_length=30)
  last_name=models.CharField(max_length=30)  # Optional handle
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)       # ✅ Required for admin access
  is_superuser = models.BooleanField(default=False)   # ✅ Usually added explicitly

   
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
        return self.username or self.email

