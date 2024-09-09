from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)    # либо verbose_name="Имя"
    last_name = models.CharField(
      'Фамилия', blank=True, help_text='Необязательное поле', max_length=20   # blank=True вместо required=False (допустимы пустые значения);
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,)) # Валидатор указывается в описании поля.
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        pass

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk}) 