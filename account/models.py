from PIL import Image
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# hook in the New Manager to our Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'profile_pictures/{user_id}/{filename}'.format(
        user_id=str(instance.user.id), filename=filename)
    return file_path


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    MEMBERSHIP_LEVEL = (
        ('fellow', 'Fellow (FAHII)'),
        ('executive', 'Executive (EAHII)'),
        ('associate', 'Associate (AAHII)'),
        ('student', 'Student (SAHII)'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name='user_profile')
    full_name = models.CharField(max_length=255)
    professional_prefix = models.CharField(max_length=20)
    # membership_id = models.CharField(max_length=25, unique=True)
    country = models.CharField(max_length=255, blank=True, null=True, default="Nigerian")
    date_of_birth = models.CharField(max_length=255, blank=True, null=True)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)
    x_url = models.CharField(max_length=255, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=False, null=True)
    membership_level = models.CharField(max_length=50, choices=MEMBERSHIP_LEVEL)
    # picture = models.ImageField(
    #     default='profile/avatar.jpg', blank=True, null=True, upload_to=upload_location)
    picture = models.ImageField(blank=True, null=True, upload_to=upload_location)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    # reduce the size of the profile image if it's more than 900px
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 500 or img.width > 1000:
                output = (400, 500)
                img.thumbnail(output)
                img.save(self.picture.path)

    @property
    def get_image_url(self):
        return self.picture.url
    
    def __str__(self):
        return self.user.email