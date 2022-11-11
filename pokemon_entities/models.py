from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень', default=0, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', default=0, blank=True)
    attack = models.IntegerField(verbose_name='Атака', default=0, blank=True)
    defence = models.IntegerField(verbose_name='Защита', default=0, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0, blank=True)

    def __str__(self):
        return f'{self.id} - {self.pokemon.title}'
