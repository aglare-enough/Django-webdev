from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    last_login = models.CharField(max_length=20,null=True)
    is_superuser = models.BooleanField()
    is_active=models.BooleanField()
    last_name=models.CharField(max_length=255,null=True)
    email=models.EmailField(max_length=255,null=True)
    is_staff = models.BooleanField()
    date_joined = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=20,null=True)
    jwt_version = models.CharField(max_length=100,null=True)
    wallet = models.BigIntegerField(null=True)

class Order(models.Model):
    pro = models.CharField(max_length=255)
    conf = models.CharField(max_length=50)
    address = models.CharField(max_length=255,null=True)
    phonenumber = models.CharField(max_length=30,null=True)
    peo = models.CharField(max_length=50,null=True)
    user_id = models.IntegerField(null=True)
    #time_joined = models.CharField(max_length=50,null=True)
    #start = models.BooleanField(default='0')
    price = models.IntegerField(default='0')


class PayedOrder(models.Model):
    pro = models.CharField(max_length=255)
    conf = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True)
    phonenumber = models.CharField(max_length=30, null=True)
    peo = models.CharField(max_length=50, null=True)
    user_id = models.IntegerField(null=True)
    time_joined = models.CharField(max_length=50, null=True)
    start = models.BooleanField(default='0')
    price = models.IntegerField(default='0')

class HisOrder(models.Model):
    pro = models.CharField(max_length=255)
    conf = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True)
    phonenumber = models.CharField(max_length=30, null=True)
    peo = models.CharField(max_length=50, null=True)
    user_id = models.IntegerField(null=True)
    time_joined = models.CharField(max_length=50, null=True)
    #start = models.BooleanField(default='0')
    price = models.IntegerField(default='0')