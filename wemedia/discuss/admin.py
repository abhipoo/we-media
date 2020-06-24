from django.contrib import admin
from .models import (Topic, context, content,
                    content_types, ask,
                    suggestion, Comment,
                    Comment_relation)

# Register your models here.
admin.site.register(Topic)
admin.site.register(context)
admin.site.register(content)
admin.site.register(content_types)
admin.site.register(ask)
admin.site.register(suggestion)
admin.site.register(Comment)
admin.site.register(Comment_relation)
