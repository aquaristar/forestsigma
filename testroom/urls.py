from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='testroom_index'),
    path('admin', views.admin, name='test_admin'),
    path('detail/<int:test_id>', views.test_detail, name='test_detail'),
    path('delete/<int:test_id>', views.test_delete, name='test_delete'),
    path('result', views.test_result, name='test_result'),
    path('save_and_new_test', views.save_and_new_test, name='save_and_new_test'),
]