from unittest.mock import patch
import os

from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework import status

from djassr import views


class APIViewsTestCase(TestCase):
    def setUp(self):
        os.environ['S3_BUCKET'] = 'a-bucket'
        os.environ['AWS_ACCESS_KEY'] = 'a-key'
        os.environ['AWS_SECRET_KEY'] = 'a-secret'
        self.factory = APIRequestFactory()

    def test_get_PUT_signature(self):
        view = views.GetPUTSignature.as_view()
        object_name = 'filename-uuid'
        file_name_extension = '.txt'
        data = {'file_name': 'a-file' + file_name_extension,
                'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = object_name
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['object_name'], object_name + file_name_extension)

    def test_get_PUT_public_signature(self):
        view = views.GetPUTPublicSignature.as_view()
        object_name = 'filename-uuid'
        file_name_extension = '.txt'
        data = {'file_name': 'a-file' + file_name_extension,
                'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = object_name
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_GET_signature(self):
        view = views.GetGETSignature.as_view()
        object_name = 'object_name.txt'
        data = {'object_name': object_name}
        request = self.factory.post('/the-view/', data=data)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_PUT_signature_optional_filename(self):
        view = views.GetPUTSignature.as_view()
        object_name = 'filename-uuid'
        data = {'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = object_name
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['object_name'], object_name)
