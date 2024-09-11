# Импортируем класс пагинатора.
# from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect #, render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm, CongratulationForm
# Импортируем модель дней рождения.
from .models import Birthday, Congratulation

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

# ИДЁТ ПОСЛЕДНИМ В СПИСКЕ КЛАССОВ 

class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):               # Переопределение  словаря контекста 
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context


# ОЧЕРЕДНАЯ ПЕРЕКОМПАНОВКА с миксинами          Есть и ещё один вариант. Можно не создавать миксин BirthdayFormMixin, а переименовать шаблон birthday/birthday.html в birthday/birthday_form.html — именно это название ожидает по умолчанию класс CreateView. 
# В этом случае в классе BirthdayCreateView название шаблона можно вообще не указывать, а в классах для создания и редактирования объектов указать не pass, а form_class = BirthdayForm. 
                                                                    # ВТОРОЙ КЛАСС
# УБРАЛИ ИЗ-ЗА  get_absolute_url(self): в моделях
# class BirthdayMixin:          
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


# class BirthdayFormMixin:           УБРАЛИ ПОСЛЕ ДитэйлВью
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'


class BirthdayCreateView(LoginRequiredMixin, CreateView):        # БЫЛ еще BirthdayFormMixin и BirthdayMixin в ()
    model = Birthday
    form_class = BirthdayForm

# задача: передать объект автора записи в объект формы; добавить объект автора в поле author нужно перед сохранением объекта формы.
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView): # БЫЛ еще BirthdayFormMixin и BirthdayMixin в ()
    model = Birthday
    form_class = BirthdayForm



# НОВЫЙ КЛАСС MIXIN.
# class BirthdayMixin:
#     model = Birthday
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'
#     success_url = reverse_lazy('birthday:list')


# # Добавляем миксин первым по списку родительских классов.
# class BirthdayCreateView(BirthdayMixin, CreateView):
#     # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
#     pass


# class BirthdayUpdateView(BirthdayMixin, UpdateView):
#     # И здесь все атрибуты наследуются от BirthdayMixin.
#     pass



# # НОВЫЙ КЛАСС РЕДАКТИРОВАНИЯ, теперь создание и редакт отдельно, а не как в def birthday(request, pk=None)

# class BirthdayUpdateView(UpdateView):
#     model = Birthday
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'
#     success_url = reverse_lazy('birthday:list') 


# НОВЫЙ КЛАСС 2.0 ЧЕРЕЗ CBV

# class BirthdayCreateView(CreateView):
#     # Указываем модель, с которой работает CBV...
#     model = Birthday
#     # Этот класс сам может создать форму на основе модели!
#     # Нет необходимости отдельно создавать форму через ModelForm.
#     # Указываем поля, которые должны быть в форме:
#             # БЫЛО fields = '__all__'  ----- подключили дату и контроль имён
#     form_class = BirthdayForm
#     # Явным образом указываем шаблон:     В приложении birthday шаблон называется иначе, так что его название нужно указать в явном виде через атрибут template_name.
#     template_name = 'birthday/birthday.html'
#     # Указываем namespace:name страницы, куда будет перенаправлен пользователь
#     # после успешного создания объекта:
#     success_url = reverse_lazy('birthday:list')     # Путь для редиректа указывается в функции reverse_lazy(): 
#                                                     # она, как и функция reverse(), возвращает строку с URL нужной страницы. 
#                                                     # НО срабатывает только при непосредственном обращении к CBV во время работы веб-сервера, 
#                                                     # а не на этапе запуска проекта, когда импортируются все классы. 
#                                                     # В момент запуска проекта карта маршрутов может быть ещё не сформирована, 
#                                                     # и использование обычного reverse() вызовет ошибку.


                     # НОВАЯ ФУН-Я С РЕДАКТИРОВАНИЕМ
# # Добавим опциональный параметр pk.
# def birthday(request, pk=None):
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None.
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None, 
#         files=request.FILES or None,        # сохранит файлы, отправленные через форму, на жёсткий диск
#         instance=instance)
#     # Остальной код без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)

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


                                                    # НОВОЕ УДАЛЕНИЕ CBV
class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    # template_name = 'birthday/birthday.html'       УБРАЛИ вызов шаблона, п/ч есть шаблон с именем, которое ожидает класс DeleteView
    success_url = reverse_lazy('birthday:list')

# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)


# НОВАЯ ВЬЮХА 

# Наследуем класс от встроенного ListView:                            ПЕРВЫЙ КЛАСС
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10

# def birthday_list(request):
#     # Получаем список всех объектов модели Birthday из БД с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаём объект пагинатора с количеством 10 записей на страницу.
#     paginator = Paginator(birthdays, 10)

#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора. 
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст 
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}  #{'birthdays': birthdays} <--- было     # Передаём их в контекст шаблона.
#     return render(request, 'birthday/birthday_list.html', context)

# Будут обработаны POST-запросы только от залогиненных пользователей.


@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)
