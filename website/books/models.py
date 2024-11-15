from django.contrib.auth.models import AbstractUser,Group
from .managers import CustomUserManager
from django.db import models

class user(AbstractUser):
	first_name=models.CharField(max_length=32,db_column='first_name')
	last_name=models.CharField(max_length=32,db_column='last_name')
	email=models.EmailField(unique=True,db_column='email')
	password=models.CharField(max_length=255,null=True,db_column='password')
	dob = models.DateField(db_column='dob')
	city = models.CharField(max_length=40,db_column='city')
	country = models.CharField(max_length=40)
	username=None
	USERNAME_FIELD='email'
	objects=CustomUserManager()
	REQUIRED_FIELDS=['dob','country','city']
	class meta:
		db_table='user'
	def __str__(self):
		return self.get_full_name()



class product(models.Model):
	upc=models.CharField(max_length=255,db_column='upc',help_text='univercel product code')
	name=models.CharField(max_length=255,db_column='name')
	type=models.CharField(max_length=30,db_column='type')
	category=models.CharField(max_length=50,null=True,db_column='category')
	description=models.TextField(null=True,db_column='description')
	stock=models.IntegerField(default=0,db_column='stock')
	price=models.FloatField(db_column='price')
	tax=models.FloatField(default=0,db_column='tax')
	rating=models.FloatField(default=5.0,db_column='rating')
	reviews=models.IntegerField(db_column='reviews')
	class meta:
		db_table='product'

class image(models.Model):
	id=models.BigAutoField(primary_key=True)
	upc=models.ForeignKey()