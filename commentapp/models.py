from django.db import models
from django.conf import settings


from postapp.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, related_name='comment_post')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='commenter')
    body = models.TextField()
    
    comment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 

    class Meta:
        ordering = ('-comment_date', )
       
    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.name, str(self.post.id)) 
