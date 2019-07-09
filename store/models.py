from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models import Sum, F, DecimalField

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user."""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email instead of username and personal info."""

    email = models.EmailField(max_length=120, unique=True)
    name = models.CharField(max_length=200)
    phone = PhoneNumberField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.name


class Entry(models.Model):
    order = models.ForeignKey('Order', related_name='entries', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f'{self.quantity} ✕ {self.product} for {self.order}'

    @property
    def price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    address = models.TextField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.name} at {self.address}'

    @property
    def total_entries(self):
        return self.entries.count()

    @property
    def total_products(self):
        return self.entries.aggregate(Sum('quantity'))['quantity__sum']

    @property
    def total_price(self):
        return self.entries.aggregate(
            total_price=Sum(F('quantity')*F('product__price'),
            output_field=DecimalField())
        )['total_price']
