from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'', admin.site.urls),
    url(r'^api/', include('zamrine_web_application.urls'))
]
