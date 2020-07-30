from django.conf.urls import url, include
from django.contrib import admin

admin.site.site_header = 'Zamrine Admin Panel'
admin.site.site_title = 'Zamrine Admin'
admin.site.index_title = '' 

urlpatterns = [
    url(r'', admin.site.urls),
    url(r'^api/', include('zamrine_web_application.urls'))
]
