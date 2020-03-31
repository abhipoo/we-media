from django.db import models

# Create your models here.
class topic(models.Model):
    '''
    need to decouple this model into two models -->

    topic -> An idea or a concept. Example : fantasy, anxiety
    Fields : title, description

    comment / thread -> Free text.
    Fields : description, is_op (initiator of discussion)

    '''
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

#separate app
class content_types(models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

class ask(models.Model):
    content_choices = models.ManyToManyField(content_types)
    description = models.CharField(max_length = 1000, default=None, blank=True, null=True)

class suggestion(models.Model):
    description = models.CharField(max_length = 10000)
    ask = models.ForeignKey(ask, on_delete = models.CASCADE)


#separate app
class Comment(models.Model):
    description = models.CharField(max_length = 10000)
    is_op = models.BooleanField()

    def __str__(self):
        return self.description

class Comment_relation(models.Model):
    source = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'sources')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'targets')
    relation_type = models.CharField(max_length = 100)




