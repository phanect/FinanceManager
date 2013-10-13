from django.db import models

class MoneyFlowItem(models.Model):
	amount	= models.BigIntegerField()
	date	= models.DateField()
	category = models.IntegerField(max_length=1)
