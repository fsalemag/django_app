import os

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
            
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    """ Custom user profile that uses email instead of username"""
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """ Model to keep properties of User profile, that are not related with login info"""
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        choices=(("f", "Female"), ("m", "Male"), ("o", "Other")),
        max_length=1,
        null=False,
        blank=False,
    )

    phone_number = models.IntegerField()

    profile_picture = models.ImageField(
        upload_to='uploads/profile_pictures/',
        default='uploads/profile_pictures/default.jpg',
    )

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_picture.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.profile_picture.path)


@receiver(pre_save, sender=UserProfile)
def remove_old_picture_if_exists(sender, **kwargs):
    new_user_profile = kwargs['instance']
    try:
        old_user_profile = UserProfile.objects.get(pk=new_user_profile.pk)
    except UserProfile.DoesNotExist:
        return None

    if old_user_profile.profile_picture:
        path = old_user_profile.profile_picture.path
        os.remove(path)
