from django.db import models

# Create your models here.
class Topic(models.Model):
    '''
    need to decouple this model into two models -->

    topic -> An idea or a concept. Example : fantasy, anxiety
    Fields : title, description

    comment / thread -> Free text.
    Fields : description, is_op (initiator of discussion)

    '''
    title = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 10000, default=None, blank=True, null=True)


    def __str__(self):
        return self.title

class context(models.Model):
    context_url = models.CharField(max_length = 1000)
    #contents = models.ManyToManyField(content)

    def __str__(self):
        return self.context_url

class content(models.Model):
    title = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    creator = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    topics = models.ManyToManyField(Topic)
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
    topics = models.ManyToManyField(Topic, blank = True, related_name = 'comments')
    contents = models.ManyToManyField(content, blank = True, related_name = 'comments')

    def __str__(self):
        return self.description

class Comment_relation(models.Model):
    source = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'sources')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'targets')
    relation_type = models.CharField(max_length = 100)




