from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('UserApp.urls'), name='user-routes'),
    path('postapi/', include('PostApp.urls'), name='Post-routes'),
    path('community/', include('CommunityApp.urls'), name='community-route'),
    path('basicapp/', include('BasicApp.urls'), name='basic-app'),
    path('request/', include('RequestApp.urls'), name='request-app'),
    path('AI/' , include('AI.urls') , name = "AI-Chat")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
