from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = AbstractBaseUser.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, username, is_superuser=True, is_staff = True, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=20, unique=True)
    objects = UserManager()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _("base user")
        verbose_name_plural = _("base users")

    @property
    def user(self):
        return User.objects.get(base_user=self)
    
class Language(TimeStampedModel):
    iso_2 = models.CharField(max_length=2)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s (%s)"%(self.name,self.iso_2)


class Place(TimeStampedModel):
    user = models.ForeignKey('api.User',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    picture =  models.ImageField(upload_to='pictures/%Y/%m/%d/')
    date_init = models.DateField()
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class File(TimeStampedModel):
    user = models.ForeignKey('api.User',on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/%Y/%m/%d/')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.file.name

class User(TimeStampedModel):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile/%Y/%m/%d/')
    short_biography = models.CharField(max_length=500)
    preferred_language = models.ForeignKey(Language,on_delete=models.CASCADE)



    def __str__(self):
        return "%s %s"%(self.first_name, self.last_name)