from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import BookstoreUser


class TestAuthentication(APITestCase):
    """
    Test register, login and logout views
    """

    def setUp(self):
        self.user = BookstoreUser.objects.create_user(email='test@email.com', password='123')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_successful_login(self):
        response = self.client.post(path='/api/login/', data={'email': 'test@email.com', 'password': '123'}, format='json')
        assert response.status_code == 200
        assert response.data.get('token') is not None

    def test_invalid_email(self):
        response = self.client.post(path='/api/login/', data={'email': 'wrong_user', 'password': '123'}, format='json')
        assert response.status_code == 404
        assert response.data['detail'] == 'Not found.'

    def test_invalid_password(self):
        response = self.client.post(path='/api/login/', data={'email': 'test@email.com', 'password': '1234'}, format='json')
        assert response.status_code == 404
        assert response.data['message'] == 'Invalid password.'

    def test_successful_register(self):
        response = self.client.post(path='/api/register/', data={'email': 'test_register@email.com', 'password': '321'},
                                    format='json')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully registered.'

        # Login with new registered user
        checking = self.client.post(path='/api/login/', data={'email': 'test_register@email.com', 'password': '321'},
                                    format='json')
        assert checking.status_code == 200

    def test_already_register(self):
        response = self.client.post(path='/api/register/', data={'email': 'test@email.com', 'password': '321'},
                                    format='json')
        assert response.status_code == 400
        assert response.data['message'] == 'User already exists.'

    def test_invalid_register_payload(self):
        response = self.client.post(path='/api/register/', data={'email': 'test', 'password': '321'},
                                    format='json')
        assert response.status_code == 400
        assert response.data['message'] == 'Invalid payload.'

    def test_logout(self):
        before_logout_token = Token.objects.get(user=self.user)
        assert before_logout_token.key == self.token.key
        response = self.client.get(path='/api/logout/')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully logged out.'
        after_logout_token = Token.objects.filter(user=self.user)
        assert not after_logout_token


