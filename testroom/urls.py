from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='testroom_index'),
    path('admin', views.admin, name='test_admin'),
    path('detail/<int:test_id>', views.test_detail, name='test_detail'),
    path('delete/<int:test_id>', views.test_delete, name='test_delete'),
]