from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email or not username:
            raise ValueError('No hay correo o usuario, ingresa nuevamente')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
class Usuario(AbstractBaseUser):
    ROLES = (
        ('admin', 'admin'),
        ('cliente', 'cliente')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=50, choices=ROLES, default='cliente')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name) ##Va a retornar en formato string, el primer nombre y el ultimo
    
    def has_perm(self, perm, obj=None):
        return self.is_admin ##Se muestra si es True, el usuario tiene permiso de todo, si es false significa que no
    
    def has_module_perms(self, add_label):
        return True ##Permite que el usuario admita a un modulo de la app de django
     
    class Meta:
        verbose_name_plural = 'Usuario' ##Cambia el nombre en plural del modelo en el panel de administración de Django.


# Create your models here.
