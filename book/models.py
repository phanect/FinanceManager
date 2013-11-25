from django.db import models
from datetime import timedelta
from datetime import datetime

class Purchase(models.Model):
	amount	= models.BigIntegerField()
	date	= models.DateField()
	category = models.IntegerField(max_length=1)

	def save(self, *args, **kwargs):
		super(Purchase, self).save(*args, **kwargs)
		RecentRegistry(purchase=self).save()

class RecentRegistry(models.Model):
	purchase = models.ForeignKey("Purchase")
	register_datetime = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		# Delete data from 3 days before
		RecentRegistry.objects.filter(register_datetime__lte=datetime.now() - timedelta(days=3)).delete()
		super(RecentRegistry, self).save(*args, **kwargs)

class Category(models.Model):
	id = models.AutoField()
	group = models.TextField()
	name = models.TextField()
