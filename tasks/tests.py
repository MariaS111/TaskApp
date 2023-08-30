from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import CustomUser
from .models import Task, Board


class BoardsTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='12345test*')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_board(self):
        response = self.client.post('/api/board/', {'title': 'Second board', 'description': 'second board'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_board(self):
        board = Board.objects.get(title='Main board')
        pk = board.pk
        response = self.client.patch(f'/api/board/{pk}/', {'description': 'second board updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_boards(self):
        response = self.client.get('/api/board/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
