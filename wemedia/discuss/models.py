from django.db import models

# Create your models here.
class topic(models.Model):
	title = models.CharField(max_length = 1000)
	description = models.CharField(max_length = 10000)
	is_op = models.BooleanField()

class relation(models.Model):
	source = models.ForeignKey(topic, on_delete=models.CASCADE)
	target_id = models.IntegerField()
	relation_type = models.CharField(max_length = 100)




