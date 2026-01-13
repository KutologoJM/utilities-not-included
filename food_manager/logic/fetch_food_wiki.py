import requests

url = "https://oxygennotincluded.wiki.gg/wiki/Food_(Resource)"
fetched_page = requests.get(url).text

with open('food_wiki.html', 'w') as f:
    f.write(fetched_page)

