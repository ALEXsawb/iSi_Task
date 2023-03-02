from typing import List, Optional

from django.contrib.auth import get_user_model
from django.db import models

AUTH_USER_MODEL = get_user_model()


class ThreadModel(models.Model):
    participant1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Учасник',
                                     related_name='participant1')
    participant2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Учасник',
                                     related_name='participant2')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Час та дата створення')
    updated = models.DateTimeField(auto_now=True, verbose_name='Час та дата оновлення')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = "Чати"

    def __str__(self):
        return f'Чат {self.participant1} та {self.participant2}'


class MessageModel(models.Model):
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Відправник(автор)')
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, verbose_name='Чат')
    text = models.TextField(max_length=250, verbose_name='Текст повідомлень')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Час та дата створення')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'

    def __str__(self):
        return self.text[:25] if len(self.text) > 25 else self.text
