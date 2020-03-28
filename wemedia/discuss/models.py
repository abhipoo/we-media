from django.db import models

# Create your models here.
class topic(models.Model):
    title = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 10000, default=None, blank=True, null=True)
    is_op = models.BooleanField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title

class relation(models.Model):
    source = models.ForeignKey(topic, on_delete=models.CASCADE)
    target_id = models.IntegerField()
    relation_type = models.CharField(max_length = 100)

class context(models.Model):
    context_url = models.CharField(max_length = 1000)
    #contents = models.ManyToManyField(content)

    def __str__(self):
        return self.context_url

class content(models.Model):
    title = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    creator = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    topics = models.ManyToManyField(topic)
    contexts = models.ManyToManyField(context)
    related_content = models.ManyToManyField("self", blank = True)

    def __str__(self):
        return self.title

    def clean(self):
        #Need to test this !!
        if not self.title and not self.creator:  # This will check for None or Empty
            raise ValidationError({'title': _('Even one of title or creator should have a value.')})


