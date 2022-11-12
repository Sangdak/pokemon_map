from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    previous_evolution = models.ForeignKey(
        'pokemon_entities.pokemon',
        related_name='next_evolution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    img_url = models.ImageField(null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    appeared_at = models.DateTimeField(blank=True)
    disappeared_at = models.DateTimeField(blank=True)
    level = models.IntegerField(verbose_name='Уровень', default=0, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', default=0, blank=True)
    attack = models.IntegerField(verbose_name='Атака', default=0, blank=True)
    defence = models.IntegerField(verbose_name='Защита', default=0, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0, blank=True)

    def __str__(self):
        return f'{self.id} - {self.pokemon.title_ru}'
