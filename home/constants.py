
### FILL COMMAND CONNSTANTS ###

MAX_PRODUCTS_KEEPED = 50
PAGE_SIZE = 60
CAT_SEARCH = "{} is being filled"
CAT_FINDING_FAIL = "only {} aliments have been found in the category {}."
CAT_FINDING_SUCCESS = "the category {} have been filled."
OFF_URL = "https://fr.openfoodfacts.org/cgi/search.pl"
PRODUCTS_FIELDS = [
    "product_name_fr",
    "nutrition_grade_fr",
    "ingredients_text_fr",
    "url",
    "image_url"
]
CATEGORIES = [
    "pizzas",
    "salades-composees",
    "fromages",
    "pates-a-tartiner",
    "cereales-pour-petit-déjeuner"
]


### SEARCH QUERY CONSTANT ###
MAX_SUBSTITUTES = 6

### TEST_SCORE CONSTANT ###
MEAN_VOTE = "Les utilisateurs de PurBeurre ont donnés la note moyenne de {} à ce produit."
NO_VOTE = "soyez le premier utilisateur à noter ce produit!"