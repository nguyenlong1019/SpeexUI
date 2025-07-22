from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from libs.models import TimeInfo 
from django.utils import timezone 
from datetime import timedelta 


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user 
    

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeInfo):
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )

    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    # is_verified = models.BooleanField(default=False) # verify by email

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    facebook = models.URLField(max_length=2000, null=True, blank=True)
    zalo = models.URLField(max_length=2000, null=True, blank=True)
    age = models.SmallIntegerField(default=18)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email 
    

    def save(self, *args, **kwargs):
        if not self.fullname:
            self.fullname = str(self.email).split('@')[0]
        super(User, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        db_table = 'users'


# class OTPVerify(TimeInfo):
#     otp_code = models.CharField(max_length=6)
#     is_verify = models.BooleanField(default=False)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # not one to one: if re send 
#     expired = models.DateTimeField(null=True, blank=True)


#     class Meta:
#         verbose_name = 'OTP Verify'
#         verbose_name_plural = 'OTP Verify'
#         db_table = 'otp_verify'


#     @property 
#     def is_expired(self):
#         return timezone.now() > self.expired
    

#     def __str__(self):
#         return f"{self.otp_code}"
    

#     def save(self, *args, **kwargs):
#         if not self.expired:
#             self.expired = timezone.now() + timedelta(minutes=5)
#         super().save(*args, **kwargs)

