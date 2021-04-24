from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View

from blog.functions import lexicon, quote, SearchForm
from .models import Hero


class WallOfHeroesView(TemplateResponseMixin, View):
    template_name = 'wall_of_heroes/my_heroes.html'

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        heroes = Hero.objects.all()
        ctx = {'section': 'my_heroes',
               'heroes': heroes,
               } | base_ctx
        return self.render_to_response(ctx)


class HeroDetailView(TemplateResponseMixin, View):
    template_name = 'wall_of_heroes/hero_detail.html'

    def get(self, *args, **kwargs):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        hero = Hero.objects.get(slug=kwargs['slug'])
        ctx = {'hero': hero} | base_ctx
        return self.render_to_response(ctx)
