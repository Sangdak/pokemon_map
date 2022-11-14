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
    pokemon = models.ForeignKey(Pokemon, related_name='entities', on_delete=models.CASCADE)
    lat = models.FloatField('Координаты, шир.')
    lon = models.FloatField('Координаты, долг.')
    appeared_at = models.DateTimeField('Время появления', blank=True)
    disappeared_at = models.DateTimeField('Время исчезновения', blank=True)
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    attack = models.IntegerField(verbose_name='Атака', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.pokemon.title_ru}'
