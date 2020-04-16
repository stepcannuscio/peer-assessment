from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser,BaseUserManager
from django.core.exceptions import ValidationError
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,name,surname,email,eagle_id,password = None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name = name,
            surname = surname,
            email = self.normalize_email(email),
            eagle_id = eagle_id
        )
        user.is_staff = False ## access to admin site
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_instructor_user(self,name,surname,email,eagle_id,password = None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name = name,
            surname = surname,
            email = self.normalize_email(email),
            eagle_id = eagle_id
        )
        user.is_staff = True
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,name,surname,email,eagle_id, password = None):
        user = self.create_user(
            name = name,
            surname = surname,
            email=email,
            eagle_id = eagle_id,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def get_by_natural_key(self,email_):
        # print(email_)
        return self.get(email=email_)

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100,unique = True)
    eagle_id = models.IntegerField(unique = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)
    objects = MyUserManager() #enables access to the methods written for managin permissions and accessing data
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname','eagle_id']
    def __str__(self):
        return self.email
    def get_short_name (self):
        return self.email
    def get_natural_key(self):
        return self.email
    def clean(self):
        if len(str(self.eagle_id)) != 8:
            raise ValidationError("Eagle ID must be 8 integers")
