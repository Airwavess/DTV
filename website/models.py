from django.db import models

class Attractions(models.Model):
	at_name = models.TextField(unique=True, primary_key=True)
	at_category = models.TextField()
	at_description = models.TextField()
	at_url = models.TextField(null=True)

	class Meta:
		ordering = ['at_category']