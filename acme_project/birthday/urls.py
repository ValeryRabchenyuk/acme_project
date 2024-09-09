from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.BirthdayCreateView.as_view(), name='create'),  # Новый маршрут через CBV           БЫЛО views.birthday
    # Новый маршрут.            БЫЛО views.birthday_list
    path('list/', views.BirthdayListView.as_view(), name='list'),
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'), # Новый путь отображения отдельного объекта(даты) 
    # редактирование записей 
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),  # Новый маршрут через CBV           БЫЛО views.birthday
    # удаление
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),  # Новый маршрут через CBV           БЫЛО views.delete_birthday
]
