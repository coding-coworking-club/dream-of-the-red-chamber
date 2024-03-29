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
	type = models.CharField(max_length=20,null=True)
	ip = models.CharField(max_length=30,null=True)
	time = models.DateTimeField()
	
	def __str__(self):
		return str(self.time)


