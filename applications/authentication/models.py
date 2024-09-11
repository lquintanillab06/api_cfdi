
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager





class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField(default= 1, blank=True, null=True)
    account_expired =  models.BooleanField(default=False)
    account_locked =   models.BooleanField(default=False)

    # apellido_materno = models.CharField(max_length=255)
    # apellido_paterno = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    nombres = models.CharField(max_length=255)
    puesto = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    numero_de_empleado = models.IntegerField(blank=True, null=True)

    enabled =  models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    password_expired =  models.BooleanField(default=False)
  
    username = models.CharField(unique=True, max_length=255)
    nip = models.CharField(max_length=12, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS= []

    objects = UserManager()

    def get_shortname(self):
        return self.username

    def get_fullname(self):
        return f"{self.nombres} {self.apellidos}"
    
    ''' def save(self, *args, **kwargs):
        if self.password is not None:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs) '''

    class Meta:
        managed = True
        db_table = 'user'