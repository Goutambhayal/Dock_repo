
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.mail import send_mail
import random

# Use Fernet key from settings.py
fernet = Fernet(settings.FERNET_KEY)

# ---------------- User Manager ----------------
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)


# ---------------- User Model ----------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    api_key = models.TextField(blank=True, null=True)
    secret_key = models.TextField(blank=True, null=True)
    client_code = models.CharField(max_length=50, blank=True, null=True)
    angelone_password = models.TextField(blank=True, null=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Required by Django auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "users_data"

    # ---- password methods (optional, AbstractBaseUser already provides them) ----
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)
        super().set_password(raw_password)

    # ---- encryption for AngelOne credentials ----
    def set_encrypted_field(self, field_name, value):
        if value:
            setattr(self, field_name, fernet.encrypt(value.encode()).decode())

    def get_decrypted_field(self, field_name):
        value = getattr(self, field_name)
        return fernet.decrypt(value.encode()).decode() if value else None

    # ---- OTP methods ----
    def generate_otp(self):
        """Generate a 6-digit OTP and send via email"""
        self.otp = str(random.randint(100000, 999999))
        self.save()

        subject = "Your OTP for AlgoTrader"
        message = f"Hello {self.username},\n\nYour OTP is: {self.otp}\nIt will expire in 10 minutes."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return self.otp

    def verify_otp(self, entered_otp):
        """Verify the entered OTP"""
        if self.otp == entered_otp:
            self.is_email_verified = True
            self.otp = None
            self.save()
            return True
        return False

    def __str__(self):
        return self.username

