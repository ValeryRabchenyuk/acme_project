from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse

from django.contrib.auth import get_user_model

# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)    # либо verbose_name="Имя"
    last_name = models.CharField(
      'Фамилия', blank=True, help_text='Необязательное поле', max_length=20   # blank=True вместо required=False (допустимы пустые значения);
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,)) # Валидатор указывается в описании поля.
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    class Meta:
        pass

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})


# комментированиe
class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(     # внешних ключ — указывает, к какому объекту Birthday относится поздравление
        Birthday,
        # если автор поздравления или запись о дне рождения будут удалены — все привязанные к ним поздравления должны автоматически удаляться:
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True) # временем создания поздравления
    author = models.ForeignKey(User, on_delete=models.CASCADE)    # внешних ключ — кто автор поздравления

    class Meta:
        ordering = ('created_at',)
