from rest_framework import serializers
from .models import Post, Comment, Like
from RequestApp.models import Request
from UserApp.models import MyUser

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'created_at', 'content', 'file', 'section', 'club']
        read_only_fields = ['created_at', 'author', 'section', 'club']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = MyUser.objects.filter(id=instance.author.id).first()
        ret['first_name'] = user.first_name
        ret['last_name'] = user.last_name
        ret['likes'] = Like.objects.filter(post_id= instance.id).count()
        ret['comment'] = Comment.objects.filter(post_id=instance.id).count()
        return ret

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'post']
        read_only_fields = ['post', 'user']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = MyUser.objects.filter(id=instance.user.id).first()
        ret['first_name'] = user.first_name
        ret['last_name'] = user.last_name
        ret['student_id'] = user.student.student_id
        return ret

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']
