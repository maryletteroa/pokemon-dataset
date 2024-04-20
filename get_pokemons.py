import json
import os

import requests

# get first generation pokemons 1-151


def download_data(out_dir_name: str, url: str, tag: str):
    if not os.path.exists(f"./{out_dir_name}"):
        os.mkdir(out_dir_name)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    data = json.loads(response_text)
    if data.get(tag):
        name = data.get(tag).get("name")
    else:
        name = data.get("name")
    outfile = f"{out_dir_name}/{name}.json"
    if not os.path.exists(outfile):
        print(tag, name)
        with open(f"{out_dir_name}/{name}.json", "w", encoding="utf-8") as outf:
            print(response_text, file=outf)
    else:
        print(tag, name, "already downloaded")


def download_pokemon_first_gen():

    for id in range(1, 152):
        url = f"https://pokeapi.co/api/v2/pokemon/{id}"

        download_data(out_dir_name="pokemons", url=url, tag="species")


def download_pokemon_species_first_gen():

    for id in range(1, 152):
        url = f"https://pokeapi.co/api/v2/pokemon-species/{id}"
        download_data(out_dir_name="pokemon_species", url=url, tag="species")


def get_data(name: str, dir_name: str):
    with open(f"{dir_name}/{name}.json", "r", encoding="utf-8") as inf:
        data = json.loads(inf.read())
    return data


def download_attributes(
    name: str, dir_name: str, tags: str, tag: str, out_dir_name: str
):
    data = get_data(name=name, dir_name=dir_name)
    if data.get(tags):
        for _ in data.get(tags):
            name = _.get(tag).get("name")
            url = _.get(tag).get("url")
    else:
        name = data.get(tag).get("name")
        url = data.get(tag).get("url")
    download_data(out_dir_name=out_dir_name, url=url, tag=tag)


def write_details(out_text: str, out_path: str):

    if os.path.exists(out_path):
        mode = "a"
    else:
        mode = "w"
    with open(out_path, mode=mode, encoding="utf-8") as outf:
        print(out_text, file=outf, end="\n")


def get_pokemon_details(pokemon_name: str, output: bool = False):
    data = get_data(name=pokemon_name, dir_name="pokemons")
    id = data.get("id")
    pokename = data.get("species").get("name")
    sprite = data.get("sprites").get("front_default")
    height = data.get("height")
    weight = data.get("weight")
    base_experience = data.get("base_experience")
    order = data.get("order")
    stats = data.get("stats")

    for stat in stats:
        stat_name = stat.get("stat").get("name")
        if stat_name == "hp":
            hp = stat.get("base_stat")
        elif stat_name == "attack":
            attack = stat.get("base_stat")
        elif stat_name == "defense":
            defense = stat.get("base_stat")
        elif stat_name == "special-attack":
            special_attack = stat.get("base_stat")
        elif stat_name == "special-defense":
            special_defense = stat.get("base_stat")
        else:
            speed = stat.get("base_stat")

    stat_text = [
        str(s) for s in [hp, attack, defense, special_attack, special_defense, speed]
    ]

    for move in data.get("moves"):
        tag = "move"
        name = move.get(tag).get("name")

        out_text = "\t".join(
            [
                str(id),
                pokename,
                sprite,
                str(height),
                str(weight),
                str(order),
                name,
                tag,
            ]
            + stat_text
            + [str(base_experience)]
        )

        if output:
            write_details(out_text, out_path="out/pokemons.tsv")

    for ability in data.get("abilities"):
        if not ability.get("is_hidden"):
            tag = "ability"
            name = ability.get(tag).get("name")
            out_text = "\t".join(
                [
                    str(id),
                    pokename,
                    sprite,
                    str(height),
                    str(weight),
                    str(order),
                    name,
                    tag,
                ]
                + stat_text
                + [str(base_experience)]
            )

            if output:
                write_details(out_text, out_path="out/pokemons.tsv")

    for type in data.get("types"):
        tag = "type"
        name = type.get("type").get("name")
        out_text = "\t".join(
            [
                str(id),
                pokename,
                sprite,
                str(height),
                str(weight),
                str(order),
                name,
                tag,
            ]
            + stat_text
            + [str(base_experience)]
        )

        if output:
            write_details(out_text, out_path="out/pokemons.tsv")


def get_pokemon_species_details(pokemon_name: str, output: bool = False):
    data = get_data(name=pokemon_name, dir_name="pokemon_species")
    base_happiness = data.get("base_happiness")
    capture_rate = data.get("capture_rate")
    habitat = data.get("habitat").get("name")
    is_baby = data.get("is_baby")
    is_legendary = data.get("is_legendary")
    is_mythical = data.get("is_mythical")
    shape = data.get("shape").get("name")
    names = data.get("names")

    if not data.get("flavor_text_entries"):
        text = ""
    else:
        for text in data.get("flavor_text_entries"):
            language = text.get("language").get("name")
            if language == "en":
                text = text.get("flavor_text").replace("\n", " ").replace("\u000c", " ")
                break

    for name in names:
        language = name.get("language").get("name")
        if language == "en":
            name_en = name.get("name")
        if language == "ja-Hrkt":
            name_jp = name.get("name")

    out_text = "\t".join(
        [
            str(e)
            for e in [
                name_en,
                name_jp,
                base_happiness,
                capture_rate,
                habitat,
                shape,
                is_baby,
                is_legendary,
                is_mythical,
                text,
            ]
        ]
    )
    if output:
        outfile = "out/pokemon_species.tsv"
        write_details(out_text, out_path=outfile)


def get_move_details(move_name: str, output: bool = False):
    data = get_data(name=move_name, dir_name="moves")
    id = data.get("id")
    name = data.get("name")
    type = data.get("type").get("name")

    if not data.get("flavor_text_entries"):
        text = ""
    else:
        for text in data.get("flavor_text_entries"):
            language = text.get("language").get("name")
            if language == "en":
                text = text.get("flavor_text").replace("\n", " ")
                break

    if not data.get("effect_entries"):
        effect = ""
        short_effect = ""
    else:
        for eff in data.get("effect_entries"):
            language = eff.get("language").get("name")
            if language == "en":
                effect = eff.get("effect").replace("\n", " ")
                short_effect = eff.get("short_effect")
                break

    out_text = "\t".join(
        [str(e) for e in [id, name, type, text, effect, short_effect, "move"]]
    )

    if output:
        outfile = "out/moves.tsv"
        write_details(out_text, out_path=outfile)


def get_ability_details(ability_name: str, output: bool = False):
    data = get_data(name=ability_name, dir_name="abilities")
    id = data.get("id")
    name = data.get("name")

    if not data.get("flavor_text_entries"):
        text = ""
    else:
        for text in data.get("flavor_text_entries"):
            language = text.get("language").get("name")
            if language == "en":
                text = text.get("flavor_text").replace("\n", " ")
                break

    if not data.get("effect_entries"):
        effect = ""
        short_effect = ""
    else:
        for eff in data.get("effect_entries"):
            language = eff.get("language").get("name")
            if language == "en":
                effect = eff.get("effect").replace("\n", " ")
                short_effect = eff.get("short_effect")
                break

    out_text = "\t".join(
        [str(e) for e in [id, name, text, effect, short_effect, "ability"]]
    )

    if output:
        outfile = "out/abilities.tsv"
        write_details(out_text, out_path=outfile)


def get_type_details(type_name: str, output: bool = False):
    data = get_data(name=type_name, dir_name="types")
    id = data.get("id")
    name = data.get("name")
    if data.get("move_damage_class"):
        move_damage_class = data.get("move_damage_class").get("name")
    else:
        move_damage_class = ""
    damage_relations = data.get("damage_relations")
    double_damage_from = damage_relations.get("double_damage_from")
    double_damage_to = damage_relations.get("double_damage_to")
    half_damage_from = damage_relations.get("half_damage_from")
    half_damage_to = damage_relations.get("half_damage_to")
    no_damage_from = damage_relations.get("no_damage_from")
    no_damage_to = damage_relations.get("no_damage_to")

    if double_damage_from:
        for ddf in double_damage_from:
            dname = ddf.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "double_damage_from",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)

    if double_damage_to:
        for ddt in double_damage_to:
            dname = ddt.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "double_damage_to",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)

    if half_damage_from:
        for hdf in half_damage_from:
            dname = hdf.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "half_damage_from",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)

    if half_damage_to:
        for hdt in half_damage_to:
            dname = hdt.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "half_damage_to",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)

    if no_damage_from:
        for ndf in no_damage_from:
            dname = ndf.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "no_damage_from",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)

    if not no_damage_to:
        for ndt in no_damage_to:
            dname = ndt.get("name")

            out_text = "\t".join(
                [
                    str(e)
                    for e in [
                        id,
                        name,
                        move_damage_class,
                        dname,
                        "no_damage_to",
                        "type",
                    ]
                ]
            )

            if output:
                outfile = "out/types.tsv"
                write_details(out_text, out_path=outfile)
