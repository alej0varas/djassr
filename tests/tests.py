try:
    from unittest import mock
except ImportError:
    import mock
import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from djassr import views

from .views import CustomS3PUTSignatureAPIView


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

        with mock.patch('djassr.views.uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = object_name
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['signed_url'])
        self.assertIsNotNone(response.data['url'])
        self.assertIsNotNone(response.data['headers'])
        self.assertIsNotNone(response.data['object_name'])
        self.assertEqual(response.data['object_name'], object_name + file_name_extension)

    def test_get_GET_signature(self):
        view = views.GetGETSignature.as_view()
        object_name = 'object_name.txt'
        data = {'object_name': object_name}
        request = self.factory.post('/the-view/', data=data)

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['signed_url'])

    def test_get_PUT_signature_optional_filename(self):
        view = views.GetPUTSignature.as_view()
        object_name = 'filename-uuid'
        data = {'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with mock.patch('djassr.views.uuid.uuid4') as mock_uuid:
            mock_uuid.return_value = object_name
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['object_name'], object_name)

    def test_call_post_post(self):
        view = CustomS3PUTSignatureAPIView.as_view()
        data = {'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with mock.patch.object(CustomS3PUTSignatureAPIView, 'custom_post', autospec=True) as mock_method:
            view(request)

        self.assertEqual(mock_method.call_count, 1)

    def test_call_customize_object_name(self):
        view = CustomS3PUTSignatureAPIView.as_view()
        data = {'mime_type': 'a-mime/type'}
        request = self.factory.post('/the-view/', data=data)

        with mock.patch.object(CustomS3PUTSignatureAPIView, 'customize_object_name', autospec=True) as mock_method:
            mock_method.return_value = 'customized'
            view(request)

        self.assertEqual(mock_method.call_count, 1)
