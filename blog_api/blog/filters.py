from django_filters import FilterSet
from .models import Post, Comment


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'date_posted': ['exact', 'gte', 'lte']
        }


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'created': ['exact', 'gte', 'lte']
        }
