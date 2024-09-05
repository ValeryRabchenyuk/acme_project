"""файл, в котором хранят код, управляющий формами"""

from django import forms


from .models import Birthday


#Изменили с forms.Form
class BirthdayForm(forms.ModelForm):

       # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
    # first_name = forms.CharField(label='Имя', max_length=20)  # полей, атрибут класса BirthdayForm
    # last_name = forms.CharField(        # текстовое поле с доп атрибутом
    #     label='Фамилия',        # аргументе label для кастомного названия полей
    #     required=False,         # делает поле необязательным (по умол всегда True)
    #     help_text='Необязательное поле'     # подсказка
    #     )
    # birthday = forms.DateField(       # поле с датой
    #     label='Дата рождения',
    #     widget=forms.DateInput(attrs={'type': 'date'})      # виджет для ввода даты должен с типом date.
    #     )
