from django.db.utils import OperationalError
from .forms import SearchForm
from .models import Lexicon, Quote, Post

import random


def lexicon():
    lexicon = Lexicon.objects.all()
    try:
        return random.choices(lexicon)[0]
    except IndexError:
        return None
    except OperationalError:
        return None


def quote():
    quotes = Quote.objects.all()
    try:
        return random.choices(quotes)[0]
    except IndexError:
        return None
    except OperationalError:
        return None


def get_random_posts(last_posts):
    posts = Post.objects.filter(status='published').order_by('?')
    random_posts = []

    try:
        for post in posts:
            if post not in list(last_posts):
                random_posts.append(post)
        return random_posts
    except OperationalError:
        return []


# base_ctx = {
#     'lexicon': lexicon(),
#     'quote': quote(),
#     'search_form': SearchForm(),
# }
