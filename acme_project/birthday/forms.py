"""файл, в котором хранят код, управляющий формами"""

from django import forms
# Импортируем класс ошибки валидации.
from django.core.exceptions import ValidationError

from .models import Birthday
# Импорт функции для отправки почты.
from django.core.mail import send_mail

# Множество с именами участников Ливерпульской четвёрки.

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'} # см. фу-ю clean(self)


#Изменили с forms.Form
class BirthdayForm(forms.ModelForm):
    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        exclude = ('author',)       #  УБРАЛИ fields = '__all__', чтобы убрать из HTML-формы поле "автор" при создании записи
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется 
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            ) 




    # # Импортируем функцию-валидатор.
    # from .validators import real_age
    # 
    # 
    # 
    # first_name = forms.CharField(label='Имя', max_length=20)  # полей, атрибут класса BirthdayForm
    # last_name = forms.CharField(        # текстовое поле с доп атрибутом
    #     label='Фамилия',        # аргументе label для кастомного названия полей
    #     required=False,         # делает поле необязательным (по умол всегда True)
    #     help_text='Необязательное поле'     # подсказка
    #     )
    # birthday = forms.DateField(       # поле с датой
    #     label='Дата рождения',
    #     widget=forms.DateInput(attrs={'type': 'date'}     # виджет для ввода даты должен с типом date.

    # В аргументе validators указываем список или кортеж 
    # валидаторов этого поля (валидаторов может быть несколько).
    #    validators=(real_age,),
    #     )
