from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from api.models import BookstoreUser, Book


class DataTestSetup(APITestCase):
    def setUp(self):
        self.user = BookstoreUser.objects.create_user(email='testingUser', password='123')
        self.client.force_authenticate(user=self.user)
        Book.objects.create(title='Test Book 1', author='Author 1', ISBN='012345', price='25')
        Book.objects.create(title='Test Book 2', author='Author 2', ISBN='543210', price='17.5')


class TestAPIWithAuthorizedUser(DataTestSetup):
    """
    Test api calls with expected responses
    """

    def test_create_book_happy_case(self):
        payload = {
            "title": "Test Book",
            "author": "A Tester",
            "ISBN": "00001",
            "price": "9.5"
        }

        response = self.client.post(path='/api/create-book/', data=payload, format='json')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully created.'
        assert response.data['book'] == {
            "title": "Test Book",
            "author": "A Tester",
            "publish_date": None,
            "ISBN": "00001",
            "price": 9.5
        }

    def test_create_book_fail_validation(self):
        payload = {
            "title": "Test Book",
            "ISBN": "00001",
            "price": "9.5"
        }

        response = self.client.post(path='/api/create-book/', data=payload, format='json')
        assert response.status_code == 400
        assert response.data['message'] == 'Payload invalid.'

    def test_get_all_books(self):
        response = self.client.get(path='/api/get-books')
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0] == {
            "id": 2,
            "title": "Test Book 2",
            "author": "Author 2",
            "publish_date": None,
            "ISBN": "543210",
            "price": 17.50
        }

    def test_get_book_by_id(self):
        response = self.client.get(path='/api/get-book/1/')
        assert response.status_code == 200
        assert response.data == {
            "id": 1,
            "title": "Test Book 1",
            "author": "Author 1",
            "publish_date": None,
            "ISBN": "012345",
            "price": 25
        }

    def test_update_book_happy_case(self):
        response = self.client.put(path='/api/update-book/1/', data={"price": 20.5}, format='json')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully updated.'

    def test_update_book_not_found_book(self):
        response = self.client.put(path='/api/update-book/10/', data={"price": 20.5}, format='json')
        assert response.status_code == 404
        assert response.data['message'] == 'The book not found'

    def test_update_book_invalid_payload(self):
        response = self.client.put(path='/api/update-book/1/', data={'title': ''}, format='json')
        assert response.status_code == 400
        assert response.data['message'] == 'Payload invalid.'

    def test_delete_book_happy_case(self):
        response = self.client.delete(path='/api/delete-book/1/')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully deleted the book'
        checking = self.client.get(path='/api/get-book/1/')
        assert checking.status_code == 404
        assert checking.data['message'] == 'The book not found'

    def test_delete_book_happy_case(self):
        response = self.client.delete(path='/api/delete-book/999/')
        assert response.status_code == 404
        assert response.data['message'] == 'Book not found.'

    def test_images_upload(self):
        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), 'red')
        image.save(image_data, format='png')
        image_data.seek(0)

        payload = {
            'book_id': 1,
            'image': SimpleUploadedFile("test.png", image_data.read(), content_type='image/png')
        }
        response = self.client.post(path='/api/upload-image/', data=payload, format='multipart')
        assert response.status_code == 200
        assert response.data['message'] == 'Successfully uploaded.'

    def test_images_fail_upload(self):
        payload = {
            'book_id': 1,
            'image': b'123'
        }
        response = self.client.post(path='/api/upload-image/', data=payload, format='multipart')
        assert response.status_code == 400
        assert response.data['message'] == 'Upload failed, form is invalid.'


class TestAPIWithAnonymousUser(DataTestSetup):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_create_book_non_authorization(self):
        response = self.client.post(path='/api/create-book/', data={"title": "Test Book"}, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_get_all_books_non_authorization(self):
        response = self.client.get(path='/api/get-books')
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0] == {
            "id": 2,
            "title": "Test Book 2",
            "author": "Author 2",
            "publish_date": None,
            "ISBN": "543210",
            "price": 17.50
        }

    def test_get_book_by_id_non_authorization(self):
        response = self.client.get(path='/api/get-book/1/')
        assert response.status_code == 200
        assert response.data == {
            "id": 1,
            "title": "Test Book 1",
            "author": "Author 1",
            "publish_date": None,
            "ISBN": "012345",
            "price": 25
        }

    def test_update_book_non_authorization(self):
        response = self.client.put(path='/api/update-book/1/', data={"price": 20.5}, format='json')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_delete_book_happy_case_non_authorization(self):
        response = self.client.delete(path='/api/delete-book/999/')
        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'
