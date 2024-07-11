from django.db import models

# Create your models here.
class users(models.Model):
	name=models.CharField(max_length=149);
	email=models.CharField(max_length=149);
	password=models.CharField(max_length=149);
	phone=models.CharField(max_length=149);

class products(models.Model):
	pid=models.CharField(max_length=149);
	URL=models.TextField();
	Category=models.CharField(max_length=249);
	name=models.TextField();
	img=models.TextField();
	description=models.TextField();

class prices(models.Model):
	pid=models.CharField(max_length=149);
	price=models.CharField(max_length=149);
	company=models.CharField(max_length=249);
	dat_e=models.CharField(max_length=149);

class pricealert(models.Model):
	pid=models.CharField(max_length=149);
	price=models.FloatField();
	email=models.CharField(max_length=149);

class notifications(models.Model):
	email=models.CharField(max_length=149);
	mesg=models.TextField();
	dat_e=models.CharField(max_length=149);
	stz=models.CharField(max_length=149);


class reviews(models.Model):
	pid=models.CharField(max_length=149);
	review=models.TextField();
	rating=models.FloatField();
	name=models.CharField(max_length=149);
	email=models.CharField(max_length=149);
	sentiment=models.CharField(max_length=149);
	



