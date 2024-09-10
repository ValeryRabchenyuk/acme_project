# для статичных страниц

# Импортируем класс TemplateView, чтобы унаследоваться от него.
from django.views.generic import TemplateView

from birthday.models import Birthday


class HomePage(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        # значение ключа — число объектов модели Birthday.
        context['total_count'] = Birthday.objects.count()
        # Возвращаем изменённый словарь контекста.
        return context

# ----- ВЕРСИЯ 2 -----


# class HomePage(TemplateView):
#     # В атрибуте template_name обязательно указывается имя шаблона,
#     # на основе которого будет создана возвращаемая страница.
#     template_name = 'pages/index.html'

# Изменить остальное соответственно:
# pages/urls.py
# from django.urls import path

# from . import views

# app_name = 'pages'

# urlpatterns = [
#     path('', views.HomePage.as_view(), name='homepage'),]



# ----- ВЕРСИЯ 1 -----

# from django.shortcuts import render


# def homepage(request):
#     return render(request, 'pages/index.html')
