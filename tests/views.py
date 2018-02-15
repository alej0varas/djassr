from djassr import views


class CustomS3PUTSignatureAPIView(views.GetPUTSignature):

    def custom_post(self, request, data):
        pass
