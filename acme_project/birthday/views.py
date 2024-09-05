from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем модель дней рождения.
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


def birthday(request):
    """при обращении к адресу birthday/ вызывается view-функция birthday(),
    (которая вызывает шаблон birthday.html)
    в которой должен быть создан экземпляр класса формы BirthdayForm.
    Этот экземпляр нужно передать в HTML-шаблон через словарь context."""
    # Создаём экземпляр класса формы.
    form = BirthdayForm(request.POST or None)        # Если есть параметры GET-запроса... передаём их в конструктор класса формы.  БЫЛО С ИФ  / ЗАМЕНА НА POST 
    
    # Добавляем его в словарь контекста под ключом form (# Передаём форму в словарь контекста:)
    context = {'form': form}   
    if form.is_valid():     # Если данные валидны... # ...вызовем функцию подсчёта дней:
        form.save() # встроенный метод save() позволяет сохранить данные из формы в БД
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})

    # Указываем нужный шаблон и передаём в него словарь контекста.
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all()
    # Передаём их в контекст шаблона.
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context) 