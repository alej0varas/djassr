from django.conf.urls import url

import djassr.views

urlpatterns = [
    url('^put_signed_url/$', djassr.views.GetPUTSignature.as_view()),
    url('^put_signed_public_url/$', djassr.views.GetPUTPublicSignature.as_view()),
    url('^get_signed_url/$', djassr.views.GetGETSignature.as_view()),
]
