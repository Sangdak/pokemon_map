from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('Название', max_length=200)
    title_en = models.CharField('Название англ.', max_length=200, blank=True)
    title_jp = models.CharField('Название яп.', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey(
        'pokemon_entities.pokemon',
        verbose_name='Из кого эволюционирует',
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    img_url = models.ImageField('Изображение', null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField('Координаты, шир.')
    lon = models.FloatField('Координаты, долг.')
    appeared_at = models.DateTimeField('Время появления', blank=True)
    disappeared_at = models.DateTimeField('Время исчезновения', blank=True)
    level = models.IntegerField(verbose_name='Уровень', default=1, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', default=1, blank=True)
    attack = models.IntegerField(verbose_name='Атака', default=11, blank=True)
    defence = models.IntegerField(verbose_name='Защита', default=1, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', default=1, blank=True)

    def __str__(self):
        return f'{self.id} - {self.pokemon.title_ru}'
