import json
from typing import Tuple, List

import bs4
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('food_wiki.html'), 'html.parser')
soup = soup.find('table')

food_content_containers = soup.find_all('tr')
food_content_containers = food_content_containers[2:]

if len(food_content_containers) != 64:
    raise ValueError('Number of food containers should be 64!')


def extract_image_url(unformatted_image_url: str) -> str:
    image_url = unformatted_image_url.rsplit('/thumb')[1].rsplit('/')[1]
    formatted_image_url = f"/images/{image_url}"
    return formatted_image_url


def format_solo_a_tag(tag):
    a_tag = tag.find('a')
    name = a_tag['title']
    wiki_url = a_tag['href']
    unformatted_image_url = a_tag.find('img')['src']
    image_url = extract_image_url(unformatted_image_url)

    return name, wiki_url, image_url


def extract_basic_info(data: bs4.Tag) -> Tuple[str, str, str]:
    a_tags = data.find_all('a')
    name = a_tags[1].string
    wiki_url = a_tags[0]['href']
    unformatted_image_url = a_tags[0].find('img')['src']
    image_url = extract_image_url(unformatted_image_url)
    return name, wiki_url, image_url


def extract_dlc_info(data: bs4.Tag) -> Tuple[str, str, str] | Tuple[None, None, None]:
    dlc_info = data.find('a')
    if not dlc_info:
        return None, None, None  # dlc_name, dlc_wiki_url, dlc_image_url
    dlc_name = dlc_info['title'].split(' is')[0]
    dlc_wiki_url = dlc_info['href']
    unformatted_dlc_image_url = dlc_info.find('img')['src']
    dlc_image_url = extract_image_url(unformatted_dlc_image_url)
    return dlc_name, dlc_wiki_url, dlc_image_url


def extract_food_quality(data: bs4.Tag) -> dict | None:
    food_quality = {}
    raw_data = repr(data.string)
    if raw_data.rfind('N/A') == 1:
        return None
    else:
        unformatted_data = data.string.split('\n')[0].split()
        quality = unformatted_data[0]
        morale_impact = unformatted_data[1].split('[')[1].split(']')[0]
        food_quality['quality'] = quality
        food_quality['morale_impact'] = morale_impact
        return food_quality


def extract_spoil_time(data: bs4.Tag) -> int | None:
    raw_data = repr(data.string)
    if raw_data.rfind('N/A') == 1:
        return None
    elif raw_data.find('Never') == 1:
        return None
    else:
        spoil_time = data.string.split('cycles')[0]
        return int(spoil_time)


def extract_kcal_per_kg(data: bs4.Tag) -> int | None:
    raw_data = repr(data.string)
    if raw_data.rfind('N/A') == 1:
        return None
    else:
        kcal_per_kg = raw_data.strip("'").split('kcal')[0]
        return int(kcal_per_kg)


def extract_ingredients_container(data: bs4.Tag):
    def extract_ingredients(list_of_filtered_tags: List[bs4.Tag]):
        """
        Returns a list of ingredients by extracting their information from the input
        """

        list_of_ingredients = []
        last_index = len(list_of_filtered_tags) - 1

        for index, filtered_tag in enumerate(list_of_filtered_tags):
            ingredient_info = {}
            if filtered_tag.name == 'hr':
                continue
            if len(filtered_tag.find_all('a')) < 2:
                name, wiki_url, image_url = format_solo_a_tag(filtered_tag)
                role = 'main'
            else:
                name, wiki_url, image_url = extract_basic_info(filtered_tag)

                if last_index == 0:
                    role = 'main'
                elif index == 0:
                    # First element: only has a next neighbor
                    if list_of_filtered_tags[index + 1].name == 'hr':
                        role = 'main'
                    else:
                        role = 'substitutable'

                elif index == last_index:
                    # Last element: only has a previous neighbor
                    if list_of_filtered_tags[index - 1].name == 'hr':
                        role = 'main'
                    else:
                        role = 'substitutable'

                else:
                    # Middle elements: has both neighbors
                    if (
                            list_of_filtered_tags[index - 1].name == 'hr'
                            and list_of_filtered_tags[index + 1].name == 'hr'
                    ):
                        role = 'main'
                    else:
                        role = 'substitutable'

            ingredient_info['name'] = name
            ingredient_info['wiki_url'] = wiki_url
            ingredient_info['image_url'] = image_url
            ingredient_info['role'] = role

            list_of_ingredients.append(ingredient_info)
        return list_of_ingredients

    unfiltered_tags = data.find_all()
    filtered_tags = []

    for tag in unfiltered_tags:
        if tag.name == 'span':
            if tag.find('a')['title'] == 'The Prehistoric Planet Pack is needed to unlock this content':
                pass
            else:
                filtered_tags.append(tag)
        elif tag.name == 'hr':
            filtered_tags.append(tag)

    ingredients = extract_ingredients(filtered_tags)

    return ingredients


def extract_ingredient_amounts(data: bs4.Tag | str) -> List[str]:
    ingredient_amounts = []
    if type(data) == str:
        return ingredient_amounts
    else:
        for string in data.stripped_strings:
            ingredient_amounts.append(string)
    return ingredient_amounts


def extract_sources(data: bs4.Tag) -> List[str]:
    sources = []

    for span in data.find_all('span'):
        source_info = {}
        if len(span.find_all('a')) < 2:
            name, wiki_url, image_url = format_solo_a_tag(span)
        else:
            name, wiki_url, image_url = extract_basic_info(span)

        source_info['name'] = name
        source_info['wiki_url'] = wiki_url
        source_info['image_url'] = image_url
        sources.append(source_info)
    return sources


def extract_food_gained(data: bs4.Tag) -> List[str]:
    food_gained = []
    for string in data.stripped_strings:
        if string.find('-') != -1:  # if - is not found in the string
            string = string.split('-')
            food_gained = string
        else:
            food_gained.append(string)
    return food_gained


def main(list_of_food_item_containers: List):
    list_of_food_items = []

    def data_assignments(headings: bs4.List[bs4.Tag], data: bs4.List[bs4.Tag]) -> dict:
        # All numbers represent list indices from the positional arguments
        name, wiki_url, image_url = extract_basic_info(headings[0])
        dlc_name, dlc_wiki_url, dlc_image_url = extract_dlc_info(headings[1])
        food_quality = extract_food_quality(data[0])
        spoil_time = extract_spoil_time(data[1])
        kcal_per_kg = extract_kcal_per_kg(data[2])
        ingredients = extract_ingredients_container(data[3])
        ingredient_amounts = extract_ingredient_amounts(data[4])
        sources = extract_sources(data[5])
        food_gained = extract_food_gained(data[6])

        compiled_food_item_data = {
            'name': name,
            'wiki_url': wiki_url,
            'image_url': image_url,
            'dlc_name': dlc_name,
            'dlc_wiki_url': dlc_wiki_url,
            'dlc_image_url': dlc_image_url,
            'food_quality': food_quality,
            'spoil_time': spoil_time,
            'kcal_per_kg': kcal_per_kg,
            'ingredients': ingredients,
            'ingredient_amounts': ingredient_amounts,
            'sources': sources,
            'food_gained': food_gained
        }

        return compiled_food_item_data

    for food_item_container in list_of_food_item_containers:
        table_heading_tags = food_item_container.find_all('th')
        table_data_tags = food_item_container.find_all('td')

        if len(table_data_tags) == 7:  # case 1
            food_item = data_assignments(table_heading_tags, table_data_tags)
            list_of_food_items.append(food_item)
        elif len(table_data_tags) == 6:  # case 2
            dummy_data = 'Dummy Data'
            table_data_tags.insert(4, dummy_data)
            food_item = data_assignments(table_heading_tags, table_data_tags)
            list_of_food_items.append(food_item)
        else:
            RuntimeError('Unrecognized case scenario')

    return list_of_food_items


if __name__ == '__main__':
    food_items = main(food_content_containers)
    print(food_items)
    with (open('compiled_food_items.json', 'w')) as f:
        json.dump(food_items, f)
