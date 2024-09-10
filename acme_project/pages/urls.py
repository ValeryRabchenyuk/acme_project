# разница в  views.homepage /  HomePage.as_view()
# изменили из-за class HomePage(TemplateView)

from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
] 

# ВЕРСИЯ 1
# from django.urls import path

# from . import views

# app_name = 'pages'

# urlpatterns = [
#     path('', views.homepage, name='homepage'),
# ]
