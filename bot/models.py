from django.db import models


class User_telegram(models.Model):
	user_id = models.CharField(max_length=200)

	def __str__(self):
		return self.user_id