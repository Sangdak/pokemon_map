import folium

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=now_time, disappeared_at__gte=now_time):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.img_url}'),
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append(
            {'pokemon_id': pokemon.id,
             'img_url': request.build_absolute_uri(f'/media/{pokemon.img_url}'),
             'title_ru': pokemon.title_ru,
             }
        )

    return render(
        request,
        'mainpage.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_on_page,
        }
    )


def show_pokemon(request, pokemon_id):
    chosen_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    next_evolution = chosen_pokemon.next_evolutions.first()
    previous_evolution = chosen_pokemon.previous_evolution
    if chosen_pokemon.previous_evolution:
        prev_evo = {'pokemon_id': chosen_pokemon.previous_evolution.id,
                    'img_url': request.build_absolute_uri(f'/media/{chosen_pokemon.previous_evolution.img_url}'),
                    'title_ru': chosen_pokemon.previous_evolution.title_ru,
                    }
    else:
        prev_evo = None

    if chosen_pokemon.next_evolutions.first():
        next_evo = {'pokemon_id': chosen_pokemon.next_evolutions.first().id,
                    'img_url': request.build_absolute_uri(f'/media/{chosen_pokemon.next_evolutions.first().img_url}'),
                    'title_ru': chosen_pokemon.next_evolutions.first().title_ru,
                    }
    else:
        next_evo = None

    pokemon_item = {
        'pokemon_id': chosen_pokemon.id,
        'img_url': request.build_absolute_uri(f'/media/{chosen_pokemon.img_url}'),
        'title_ru': chosen_pokemon.title_ru,
        'title_en': chosen_pokemon.title_en,
        'title_jp': chosen_pokemon.title_jp,
        'description': chosen_pokemon.description,
        'previous_evolution': prev_evo,
        'next_evolution': next_evo,
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now_time = localtime()
    for pokemon_entity in chosen_pokemon.entities.filter(appeared_at__lte=now_time, disappeared_at__gte=now_time):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.img_url}'),
        )

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon_item,
            }
        )
