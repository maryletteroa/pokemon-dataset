import os
from glob import glob

from get_pokemons import (
    download_attributes,
    download_pokemon_first_gen,
    download_pokemon_species_first_gen,
    get_ability_details,
    get_move_details,
    get_pokemon_details,
    get_pokemon_species_details,
    get_type_details,
)

# download the pokemon json files
download_pokemon_first_gen()
download_pokemon_species_first_gen()

for i, file in enumerate(glob("pokemons/*.json"), start=1):
    pokemon_name = os.path.basename(file).split(".")[0]
    print("-----------", i, pokemon_name, "-----------")

    # download moves
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="moves",
        tag="move",
        out_dir_name="moves",
    )

    # download abilities
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="abilities",
        tag="ability",
        out_dir_name="abilities",
    )

    # download types (pokemons)
    download_attributes(
        name=pokemon_name,
        dir_name="pokemons",
        tags="types",
        tag="type",
        out_dir_name="types",
    )


for i, file in enumerate(glob("moves/*.json"), start=1):
    move_name = os.path.basename(file).split(".")[0]
    print("-----------", i, move_name, "-----------")
    # download types (moves)
    download_attributes(
        name=move_name,
        dir_name="moves",
        tags="types",
        tag="type",
        out_dir_name="types",
    )


for i, file in enumerate(glob("pokemons/*.json"), start=1):
    pokemon_name = os.path.basename(file).split(".")[0]
    print("-----------", i, pokemon_name, "-----------")
    # get_pokemon_details(pokemon_name=pokemon_name, output=True)
    get_pokemon_species_details(pokemon_name, output=True)


for i, file in enumerate(glob("moves/*.json"), start=1):
    move_name = os.path.basename(file).split(".")[0]
    print("-----------", i, move_name, "-----------")
    get_move_details(move_name=move_name, output=True)


for i, file in enumerate(glob("abilities/*.json"), start=1):
    ability_name = os.path.basename(file).split(".")[0]
    print("-----------", i, ability_name, "-----------")
    get_ability_details(ability_name=ability_name, output=True)


for i, file in enumerate(glob("types/*.json"), start=1):
    type_name = os.path.basename(file).split(".")[0]
    print("-----------", i, type_name, "-----------")
    get_type_details(type_name=type_name, output=True)
