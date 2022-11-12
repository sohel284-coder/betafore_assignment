from django.db import models
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField()
    liked = models.BooleanField(default=False)

    post_date = models.DateTimeField(auto_now_add=True, )
    update_date = models.DateTimeField(auto_now=True, )


    class Meta:
        ordering = ('-post_date', )




class Like(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name='like_post')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='liker')

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)

