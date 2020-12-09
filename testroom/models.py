from django.db import models

# Create your models here.

class Item(models.Model):
	item_id = models.AutoField(primary_key=True)
	label = models.CharField(max_length=500)	

class Subscale(models.Model):
	subscale_id = models.AutoField(primary_key=True)
	label = models.CharField(max_length=500)

class ItemChoice(models.Model):
	choice_id = models.AutoField(primary_key=True)
	label = models.CharField(max_length=500)
	value = models.IntegerField()

class Test(models.Model):
	test_id = models.AutoField(primary_key=True)
	user_ip = models.CharField(max_length=500)
	value = models.IntegerField(default=0)

class TestItem(models.Model):
	test_id = models.ForeignKey('Test', db_column='test_id', on_delete=models.CASCADE)
	item_id = models.ForeignKey('Item', db_column='item_id', on_delete=models.CASCADE)
	choice_id = models.ForeignKey('ItemChoice', db_column='choice_id', on_delete=models.CASCADE)