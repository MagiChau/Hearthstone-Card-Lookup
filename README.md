# HearthstoneCardLookup
Searcher for a Hearthstone Card based on a Search Query.
It does not handle choosing card data versus hero data for cards like Ragnaros.
I just use a card dictionary with all non-collectible cards trimmed out.

Inspired by aca20031's Hearthstone Card Bot
https://github.com/aca20031/hsbot

#Example
```
import sys
import json
from searcher import Searcher

f_read = open("cards.json", encoding = "utf8")
card_dict = json.loads(str(f_read.read()))
f_read.close()

card_searcher = Searcher(card_dict)
result = card_searcher.find_card("Al'Akir")
print(result)
```