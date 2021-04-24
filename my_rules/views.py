from django.views.generic.base import TemplateResponseMixin, View

from blog.functions import lexicon, quote, SearchForm

from .models import Rules


class MyRulesView(TemplateResponseMixin, View):
    template_name = 'my_rules/my_rules.html'

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        rules = Rules.objects.all()
        ctx = {'section': 'my_rules',
               'rules': rules,
               } | base_ctx
        return self.render_to_response(ctx)
