from djassr import views


class CustomS3PUTSignatureAPIView(views.GetPUTSignature):

    def custom_post(self, request, data):
        pass

    def customize_object_name(self, object_name):
        return object_name
