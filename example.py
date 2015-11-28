import json
from card_lookup.searcher import Searcher

f_read = open("cards.json", encoding = "utf8")
card_dict = json.loads(str(f_read.read()))
f_read.close()

card_searcher = Searcher(card_dict)
result = card_searcher.find_card("Al'Akir")
print(result)