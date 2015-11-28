"""
Completes Hearthstone Card Lookup through comparing search queries to card names
"""
import copy


class Searcher:

	def __init__(self, card_dict):
		"""Initializes a Searcher object with a card dictionary provided

		Args: card_dict(dict): Card dictionary with cards are separated
		into sub dictionaries by set and names are located in a key named 'name'
		"""

		self.card_dict = copy.deepcopy(card_dict)

	def change_card_dict(self, card_dict):
		"""Replaces the currently used card dictionary with a deep copy of another

		Args: card_dict(dict): Card dictionary with cards are separated
		into sub dictionaries by set and names are located in a key named 'name'
		"""

		self.card_dict = copy.deepcopy(card_dict)


	def find_card(self, query):
		"""Finds the best matching card and returns its information

		Args: query(string): Search query to use for lookup

		Returns:
			dict: Card information of best matching card
			None: If no suitable matches were found return None
		"""
		results = self._find_matches(query, 0.5)

		if len(results) > 0:
			results.sort(key=lambda result: result[1], reverse=True)
			return results[0][0]
		else:
			return None

	def _find_matches(self, query, min_match):
		"""Finds all cards matching a query and returns them

		Args: 
			query(string): Search query to use for lookup
			min_match(number): Minimum value for a card to be matched.
			Value can range from 0 to 1.

		Returns:
			list: List of unsorted lists containing card information then its match percent
		"""
		result_list = []
		l_query = query.lower()

		#The card dictionary main keys are the sets card belongs to
		for exp in self.card_dict:
			for card in self.card_dict[exp]:
				#Change all uppercase letters to lowercase in preparation for string comparisons
				l_cardname = card['name'].lower()

				percent_match = 0

				search_words = {}

				#Create a sub dictionary for each search word in the query
				for word in l_query.split(' '):
					search_words.update({word : {}})

				card_words = l_cardname.split(' ')

				#Calculate the match percentage between every search word and every card word
				for search_word in search_words:
					for card_word in card_words:
						match = 1 - (Searcher.levenshtein_distance(search_word, card_word) / 
							max(len(search_word), len(card_word)))

						if search_word not in search_words.keys():
							search_words[search_word] = {card_word: { 'match' : match } }
						else:
							search_words[search_word].update( {card_word: { 'match' : match } } )

				#Calculates the total match mercentage for the entire query and the card name
				for search_word in search_words:

					max_value_key = list(search_words[search_word].keys())[0]
					max_value = search_words[search_word][max_value_key]

					for card_word in search_words[search_word]:
						if search_words[search_word][card_word]['match'] > max_value['match']:
							max_value_key = card_word
							max_value = search_words[search_word][card_word]

					percent_card_match = len(max_value_key) / len(l_cardname.replace(" ", ""))
					percent_query_match = len(search_word) / len(l_query.replace(" ", ""))

					#These weights emphasizes matching the query more than the entire card
					card_match_weight = 0.25
					query_match_weight = 1 - card_match_weight

					percent_match += (percent_query_match * max_value['match'] * query_match_weight + 
						percent_card_match * max_value['match'] * card_match_weight)

				if percent_match >= min_match:
					result_list.append([card, percent_match])

		return result_list

	def levenshtein_distance(s1,s2):
		"""Levenshtein Distance Algorithm taken from Wikibooks

		Args:
			s1(string): First string for comparisons
			s2(string): Second string for comparisons

		Returns:
			int: The levenshtein distance between two strings
		"""

		if len(s1) < len(s2):
			return Searcher.levenshtein_distance(s2, s1)

		# len(s1) >= len(s2)
		if len(s2) == 0:
			return len(s1)

		previous_row = range(len(s2) + 1)
		for i, c1 in enumerate(s1):
			current_row = [i + 1]
			for j, c2 in enumerate(s2):
				insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
				deletions = current_row[j] + 1       # than s2
				substitutions = previous_row[j] + (c1 != c2)
				current_row.append(min(insertions, deletions, substitutions))
			previous_row = current_row
		
		return previous_row[-1]