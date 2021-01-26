from .forms import SearchForm
from .models import Lexicon, Quote, Post

# from PIL import Image
import random


def lexicon():
    lexicon = Lexicon.objects.all()
    try:
        return random.choices(lexicon)[0]
    except IndexError:
        return None


def quote():
    quotes = Quote.objects.all()
    try:
        return random.choices(quotes)[0]
    except IndexError:
        return None


def get_random_posts(last_posts):
    posts = Post.objects.filter(status='published').order_by('?')
    random_posts = []

    for post in posts:
        if post not in list(last_posts):
            random_posts.append(post)

    return random_posts


# def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
#     """
#     Функция для обрезки изображения по центру.
#     """
#     img_width, img_height = pil_img.size
#     return pil_img.crop(((img_width - crop_width) // 2,
#                          (img_height - crop_height) // 2,
#                          (img_width + crop_width) // 2,
#                          (img_height + crop_height) // 2))
#
#
# def crop_max_square(pil_img):
#     return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


base_ctx = {
    'lexicon': lexicon(),
    'quote': quote(),
    'search_form': SearchForm(),
}
