from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
        return f'{self.title}'

class context(models.Model):
    context_url = models.CharField(max_length = 1000)
    #contents = models.ManyToManyField(content)

    def __str__(self):
        return f'{self.context_url}'

class content(models.Model):
    title = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    creator = models.CharField(max_length = 1000, default=None, blank=True, null=True)
    topics = models.ManyToManyField(Topic)
    contexts = models.ManyToManyField(context)
    related_content = models.ManyToManyField("self", blank = True)

    def __str__(self):
        return f'{self.title}'

#separate app
class content_types(models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return f'{self.title}'

class ask(models.Model):
    content_choices = models.ManyToManyField(content_types, blank=True)
    description = models.TextField(max_length = 1000, default="", blank=True, null=True)
    image = models.ImageField(upload_to="ask_images", default="default.jpg", blank=True)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.description}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     with Image.open(self.image.path) as img:
    #         if img.height > 300 or img.width > 300:
    #             output_size =(300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)

class suggestion(models.Model):
    description = models.TextField()
    ask = models.ForeignKey(ask, on_delete = models.CASCADE)


#separate app
class Comment(models.Model):
    description = models.TextField()
    is_op = models.BooleanField()
    topics = models.ManyToManyField(Topic, blank = True, related_name = 'comments')
    contents = models.ManyToManyField(content, blank = True, related_name = 'comments')
    author = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)

    def __str__(self):
        return f'{self.description}'

class Comment_relation(models.Model):
    source = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'sources')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'targets')
    relation_type = models.CharField(max_length = 100)

    def __str__(self):
        return f'{self.related_type}'




