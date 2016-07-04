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
        data = {'file_name': 'a-file.txt',
                'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.s3sign.S3PUTSigner.get_signed_url') as mock_signer:
            mock_signer.return_value = {'canary': True}
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('canary', response.data)
        mock_signer.assert_called_once_with(
            data['file_name'], data['mime_type'], views.DEFAULT_VALID)

    def test_get_PUT_public_signature(self):
        view = views.GetPUTPublicSignature.as_view()
        data = {'file_name': 'a-file.txt',
                'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.s3sign.S3PUTPublicSigner.get_signed_url') as mock_signer:
            mock_signer.return_value = {'canary': True}
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('canary', response.data)
        mock_signer.assert_called_once_with(
            data['file_name'], data['mime_type'], views.DEFAULT_VALID)

    def test_get_GET_signature(self):
        view = views.GetGETSignature.as_view()
        object_name = 'object_name.txt'
        data = {'object_name': object_name}
        request = self.factory.post('/the-view/', data=data)

        with patch('djassr.views.s3sign.S3GETSigner.get_signed_url') as mock_signer:
            mock_signer.return_value = {'canary': True}
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('canary', response.data)
        mock_signer.assert_called_once_with(object_name, views.DEFAULT_VALID)
