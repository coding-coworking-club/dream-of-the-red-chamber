from django.db import models
from django.conf import settings
from apps.course.models import Post


class History(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='history',
        on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	course= models.ForeignKey(
		Post,
		related_name='history',
        on_delete=models.CASCADE
	)
	keyword = models.TextField()
	time = models.DateTimeField()
	ip = models. GenericIPAddressField(default = "127.0.0.1",blank=True, null=True)
	level = models.TextField(default="") # "click" or "favorite"

	def __str__(self):
		return str(self.time)


