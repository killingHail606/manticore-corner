from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.views import View

from authorization.forms import LoginForm, RegistrationForm
from .functions import quote, lexicon


class BaseMixin(View):
    form_registration = RegistrationForm()
    form_login = LoginForm()

    section = None
    add_dict = {}

    template = None

    def post(self, request):
        if 'login' in request.POST:
            self.form_login = LoginForm(request.POST)
            if self.form_login.is_valid():
                cd = self.form_login.cleaned_data
                user = authenticate(request,
                                    username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, self.template, {'section': self.section,
                                                               'form_login': self.form_login,
                                                               'form_registration': self.form_registration,
                                                               'lexicon': lexicon(),
                                                               'quote': quote()} | self.add_dict)
                else:
                    return HttpResponse('Fuck...')

        if 'logout' in request.POST:
            logout(request)
            return render(request, self.template, {'section': self.section,
                                                   'form_login': self.form_login,
                                                   'form_registration': self.form_registration,
                                                   'lexicon': lexicon(),
                                                   'quote': quote()} | self.add_dict)

        if 'registration' in request.POST:
            form_registration = RegistrationForm(request.POST)
            if form_registration.is_valid():
                cd = form_registration.cleaned_data
                User.objects.create_user(cd['username'], cd['email'], cd['password1'])
                user = authenticate(request,
                                    username=cd['username'],
                                    password=cd['password1'])
                if user is not None:
                    if user.is_active:
                        login(request, user)


    def get(self, request, slug=None):

        return render(request, self.template, {'section': self.section,
                                               'form_login': self.form_login,
                                               'form_registration': self.form_registration,
                                               'lexicon': lexicon(),
                                               'quote': quote()} | self.add_dict
                      )