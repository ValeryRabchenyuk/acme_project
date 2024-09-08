from django.shortcuts import get_object_or_404, redirect, render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем модель дней рождения.
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


                    # НОВАЯ ФУН-Я С РЕДАКТИРОВАНИЕМ
# Добавим опциональный параметр pk.
def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(
        request.POST or None, 
        files=request.FILES or None,        # сохранит файлы, отправленные через форму, на жёсткий диск
        instance=instance)
    # Остальной код без изменений.
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)

# def birthday(request):
#     """при обращении к адресу birthday/ вызывается view-функция birthday(),
#     (которая вызывает шаблон birthday.html)
#     в которой должен быть создан экземпляр класса формы BirthdayForm.
#     Этот экземпляр нужно передать в HTML-шаблон через словарь context."""
#     instance = get_object_or_404(Birthday, pk=pk)  
#     # Создаём экземпляр класса формы.
#     form = BirthdayForm(request.POST or None, instance=instance)        # Если есть параметры GET-запроса... передаём их в конструктор класса формы.  БЫЛО С ИФ  / ЗАМЕНА НА POST 
    
#     # Добавляем его в словарь контекста под ключом form (# Передаём форму в словарь контекста:)
#     context = {'form': form}   
#     if form.is_valid():     # Если данные валидны... # ...вызовем функцию подсчёта дней:
#         form.save() # встроенный метод save() позволяет сохранить данные из формы в БД
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         context.update({'birthday_countdown': birthday_countdown})

#     # Указываем нужный шаблон и передаём в него словарь контекста.
#     return render(request, 'birthday/birthday.html', context)


                                                    # УДАЛЕНИЕ
def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all()
    # Передаём их в контекст шаблона.
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context) 