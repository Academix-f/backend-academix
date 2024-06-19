from django.urls import path
from .import views

urlpatterns = [
      path('create',views.create_request , name = 'create-request'),
      path('all',views.get_all_requests, name='get-all-request'),
      path('<int:id>/delete',views.delete_request, name='delete-request'),
      path('report/create',views.create_report, name='create-report'),
      path('all',views.get_all_requests, name='get-all-request'),
      path('<int:id>/delete',views.delete_request, name='delete-request'),
      path('report/create',views.create_report, name='create-report'),
      path('report/pending',views.get_pending_report, name='get-pending-report'),
      path('report/all',views.get_all_report, name='get-all-report'),
      path('report/<int:id>/delete',views.delete_report, name='delete-report'),
      path('<int:id>/notification',views.delete_notfications, name='delete-notification'),
      path('notification',views.get_notfications, name='get-notification'),
]

