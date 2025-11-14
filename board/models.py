from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import board

# Create your models here.
class Board(models.Model):
    title=models.CharField(max_length=20)
    content = models.TextField(blank=True)
    # writer=models.CharField(max_length=20,null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(default=timezone.now)
    generation=models.CharField(max_length=20,default='10대')

    def __str__(self):
        return self.title

class Comments(models.Model):
    board_comment = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    # related_name='comments' : post.comments.all()을 통해 comments에 접근할 수 있음
    content_comment = models.TextField()  # 댓글 입력 필드
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    date_comment = models.DateTimeField(
        default=timezone.now)  # default=timezone.now로 설정되어 있으므로 저장할 때 자동으로 들어감. 사용자가 입력하지도 뷰에서 따로 설정하지도 않음.

    def __str__(self):
        return f'Comment by {self.user_comment.username} on {self.board_comment.title}'