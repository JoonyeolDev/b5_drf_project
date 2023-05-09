from django.contrib import admin
from posts.models import Posting, Comment

# Register your models here.

admin.site.register(Posting)
admin.site.register(Comment)
