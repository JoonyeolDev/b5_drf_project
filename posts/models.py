from django.db import models
from users.models import User
from django.core.validators import FileExtensionValidator


class Posting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    image = models.ImageField("이미지", null=True, upload_to="", blank=True)

    class Meta:
        def __str__(self):
            return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content = models.TextField("내용")
    created_at = models.DateTimeField("댓글 생성일", auto_now_add=True)
    updated_at = models.DateTimeField("댓글 수정일", auto_now=True)

    class Meta:
        def __str__(self):
            return f"{self.posting}'s comment {self.pk}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    created_at = models.DateTimeField("추천일", auto_now_add=True)
