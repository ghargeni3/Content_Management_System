import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import User


class UserTest(APITestCase):

    """ Test module for User """
    def setUp(self):
        url = reverse('register')
        payload={'email': 'admin@gmail.com',
                    'password': '123123Aa',
                    'role': '1',
                    'full_name': 'Admin One',
                    'phone': '+919867993572',
                    'address': 'Pune',
                    'city': 'Pune',
                    'state': 'Maharashtra',
                    'country': 'India',
                    'pincode': '415309'}

        self.client.post(url, payload, format='json')
        client = APIClient()
        url = reverse('register')
        payload={'email': 'author@gmail.com',
                    'password': '123123Aa',
                    'role': '2',
                    'full_name': 'Author One',
                    'phone': '+919867993572',
                    'address': 'Pune',
                    'city': 'Pune',
                    'state': 'Maharashtra',
                    'country': 'India',
                    'pincode': '415309'}

        client.post(url, payload, format='json')

    def test_login(self):
        """ Test if a user can login and get a JWT response token """
        url = reverse('login')
        payload = {
            "email": "admin@gmail.com",
            "password": "123123Aa"
            }
        response = self.client.post(url, payload,  format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['success'], True)
        self.assertTrue('access' in response_data)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        payload={'email': 'author1@gmail.com',
                    'password': '123123Aa',
                    'role': '2',
                    'full_name': 'Author One',
                    'phone': '+919867993572',
                    'address': 'Pune',
                    'city': 'Pune',
                    'state': 'Maharashtra',
                    'country': 'India',
                    'pincode': '415309'}

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_all_users_as_admin(self):
        """ Test fetching all users. Not Restricted to admins """
        # Setup the token
        url = reverse('login')
        payload = {'email': 'admin@gmail.com', 'password': '123123Aa'}
        response = self.client.post(url, payload, format='json')
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        # Test the user count
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(reverse('users'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), len(response_data['users']))
    
    def test_list_all_users_access_denied_as_author(self):
        """ Test fetching all users. Not Restricted to admins """
        # Setup the token
        url = reverse('login')
        payload = {'email': 'author@gmail.com', 'password': '123123Aa'}
        response = self.client.post(url, payload, format='json')
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        # Test the user count
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(reverse('users'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'You are not authorized to perform this action')
    
    def test_add_content_as_author(self):
        """ Test fetching all users. Not Restricted to admins """
        # Setup the token
        url = reverse('login')
        payload = {'email': 'author@gmail.com', 'password': '123123Aa'}
        response = self.client.post(url, payload, format='json')
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        # Test the create content
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('create_content')

        fp = open('D://Zeamo//assignment//role_based_auth//django-rest-role-jwt//api//tst_upload_files//Invoice-A59EEC46-0002.pdf','rb')
        file = InMemoryUploadedFile(
            fp, 'document', "Invoice-A59EEC46-0002.pdf", ".pdf",
            0, charset=None)

        payload={
                    "title": "Author1.1 title",
                    "body": "Author1.1 body",
                    "summury": "Author1.1 summery",
                    "categories": "Author1.1 political content",
                    "document": file
                }
        response = client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Content successfully Added!')
        self.assertEqual(response.data['content']['title'], 'Author1.1 title')
        self.assertEqual(response.data['content']['author'], 'author@gmail.com')

    def test_get_content_as_author(self):
        """ Test fetching all users. Not Restricted to admins """
        # Setup the token
        url = reverse('login')
        payload = {'email': 'author@gmail.com', 'password': '123123Aa'}
        response = self.client.post(url, payload, format='json')
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        author_token = login_response_data['access']

        #Add Content as Author
        client1 = APIClient()
        client1.credentials(HTTP_AUTHORIZATION='Bearer ' + author_token)
        fp = open('D://Zeamo//assignment//role_based_auth//django-rest-role-jwt//api//tst_upload_files//Invoice-D5E30192-0002.pdf','rb')
        file = InMemoryUploadedFile(
            fp, 'document', "Invoice-061733D2-0003.pdf", ".pdf",
            0, charset=None)

        payload={
                    "title": "Author1.2 title",
                    "body": "Author1.2 body",
                    "summury": "Author1.2 summery",
                    "categories": "Author1.2 political content",
                    "document": file
                }
        response = client1.post(reverse('create_content'), payload)
        
        # Test the get contents
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + author_token)
        response_ = client.get(reverse('contents'))

        self.assertEqual(response_.status_code, status.HTTP_200_OK)
        self.assertEqual(response_.data['message'], 'Successfully fetched contents')
        self.assertEqual(len(response_.data['contents']), 1)
