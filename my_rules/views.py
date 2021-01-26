from django.views.generic.base import TemplateResponseMixin, View

from blog.functions import base_ctx

from .models import Rules


class MyRulesView(TemplateResponseMixin, View):
    template_name = 'my_rules/my_rules.html'

    def get(self, request):
        rules = Rules.objects.all()
        ctx = {'section': 'my_rules',
               'rules': rules,
               } | base_ctx
        return self.render_to_response(ctx)
