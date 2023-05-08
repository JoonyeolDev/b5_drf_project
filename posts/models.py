from django.db import models

# Create your models here.
class Posting(models.Model):
    title = models.CharField("제목", max_length=50)
    posting_content = models.TextField("내용")
    created_at =  models.DateTimeField("생성일", auto_now_add=True)
    updated_at =  models.DateTimeField("수정일", auto_now=True)
    posting_image = models.ImageField("이미지", null=True, upload_to="", blank=True)
    