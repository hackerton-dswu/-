from rest_framework import serializers
from .models import Board, Comments


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'title', 'content', 'generation', 'user')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields=('id','board_comment','content_comment','user_comment','date_comment')