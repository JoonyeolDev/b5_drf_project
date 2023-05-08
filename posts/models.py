from django.db import models
from users.models import User

# Create your models here.
class Posting(models.Model):
    class Meta:
        def __str__(self):
            return self.title
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    image = models.ImageField("이미지", null=True, upload_to="", blank=True)
