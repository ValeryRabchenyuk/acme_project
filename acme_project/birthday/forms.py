"""файл, в котором хранят код, управляющий формами"""

from django import forms


class BirthdayForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=20)  # полей, атрибут класса BirthdayForm
    last_name = forms.CharField(        # текстовое поле с доп атрибутом
        label='Фамилия',        # аргументе label для кастомного названия полей
        required=False,         # делает поле необязательным (по умол всегда True)
        help_text='Необязательное поле'     # подсказка
        )
    birthday = forms.DateField(       # поле с датой
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})      # виджет для ввода даты должен с типом date.
        )
