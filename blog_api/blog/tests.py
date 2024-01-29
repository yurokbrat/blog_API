from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post, Comment


class BlogAPITestCase(TestCase):
    # Начальные данные для тестирования
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, text='Test Comment', author=self.user)
        self.client = APIClient()

    # Проверка создания поста
    def test_post_create(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, 'Test Post')

    # Проверка создания комментария
    def test_comment_create(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, 'Test Comment')

    # Проверка просмотра комментариев
    def test_authentication_get(self):
        response = self.client.get('/api/v1/comments/')
        self.assertEqual(response.status_code, 200)

    # Проверка добавления комментариев для неаутентифицированного пользователя
    def test_authentication_post(self):
        response = self.client.post('/api/v1/comments/', {'posts': self.post.id, 'text': 'New Comment'})
        self.assertEqual(response.status_code, 401)

    # Проверка изменения поста для неаутентифицированного пользователя
    def test_authentication_update(self):
        response = self.client.put('/api/v1/posts/', {'posts': self.post.id, 'text': 'New Comment'})
        self.assertEqual(response.status_code, 401)

    # Проверка удаления поста для неаутентифицированного пользователя
    def test_authentication_delete(self):
        response = self.client.delete('/api/v1/posts/', {'posts': self.post.id, 'text': 'New Comment'})
        self.assertEqual(response.status_code, 401)

    # Проверка защиты от чрезмерных запросов
    def test_rate_limit(self):
        for _ in range(31):
            response = self.client.get('/api/v1/posts/')
            if response.status_code == 429:
                break
        self.assertEqual(response.status_code, 429)
