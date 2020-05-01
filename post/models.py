from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('postcheck', args=[str(self.pk)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150, verbose_name='comment')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.user.username}"
