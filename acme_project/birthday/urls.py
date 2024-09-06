from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    # Новый маршрут.
    path('list/', views.birthday_list, name='list'),
    # редактирование записей 
    path('<int:pk>/edit/', views.birthday, name='edit'),
    # удаление
    path('<int:pk>/delete/', views.delete_birthday, name='delete'),
]
