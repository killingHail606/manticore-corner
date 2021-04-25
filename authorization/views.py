from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.views import View

from blog.functions import lexicon, quote, SearchForm

from .forms import LoginForm, RegistrationForm, ProfileAvatarForm, ProfileInfoForm, NewslettersForm
from .models import Profile


class Login(View):
    form_login = LoginForm()
    template = 'authorization/login.html'

    def post(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        self.form_login = LoginForm(request.POST)
        if self.form_login.is_valid():
            cd = self.form_login.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:main_blog')
            else:
                return render(request, self.template, {'form_login': self.form_login} | base_ctx)

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        return render(request, self.template, {'form_login': self.form_login} | base_ctx)


class Registration(View):
    form_registration = RegistrationForm()
    template = 'authorization/registration.html'

    def post(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        self.form_registration = RegistrationForm(request.POST)
        if self.form_registration.is_valid():
            cd = self.form_registration.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])

            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password1'])
            Profile.objects.create(user_id=user.id, email_newsletters=cd['email_newsletters'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:main_blog')
        else:
            return render(request, self.template, {'form_registration': self.form_registration} | base_ctx)

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        return render(request, self.template, {'form_registration': self.form_registration} | base_ctx )


def save_profile(backend, user, response, *args, **kwargs):
    try:
        profile_user = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        Profile.objects.create(user_id=user.id)



class UserPageView(View):
    def post(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        profile_user = Profile.objects.get(user=request.user)
        avatar_form = ProfileAvatarForm(instance=Profile)
        info_form = ProfileInfoForm(instance=request.user)
        newsletters_form = NewslettersForm(instance=Profile)
        profile_user = Profile.objects.get(user=request.user)

        if 'info' in request.POST:
            info_form = ProfileInfoForm(instance=request.user, data=request.POST)
            user = User.objects.get(username=request.user.username)

            if info_form.is_valid():
                info_form.save()
                return redirect('authorization:user_page')
            else:
                return render(request, 'authorization/user_page.html', {
                    'profile_user': profile_user,
                    'avatar_form': avatar_form,
                    'info_form': info_form,
                    'newsletters_form': newsletters_form,
                } | base_ctx)

        if 'avatar' in request.POST:
            profile = Profile.objects.get(user=request.user)

            avatar_form = ProfileAvatarForm(instance=profile, data=request.POST, files=request.FILES)

            if avatar_form.is_valid():
                profile.picture = avatar_form.files['picture']
                profile.save_avatar()
                messages.success(request, 'Profile updated successfully')
                return redirect('authorization:user_page')
            else:
                return redirect('authorization:user_page')

        if 'newsletters' in request.POST:
            profile = Profile.objects.get(user=request.user)
            newsletters_form = NewslettersForm(instance=profile, data=request.POST)

            if newsletters_form.is_valid():
                newsletters_form.save()
                return redirect('authorization:user_page')
            else:
                messages.error(request, 'Error updating your profile')
                
        if 'logout' in request.POST:
            logout(request)
            return redirect('blog:main_blog')

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        try:
            profile_user = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            logout(request)
            return redirect('blog:main_blog')
        avatar_form = ProfileAvatarForm(instance=profile_user)
        info_form = ProfileInfoForm(instance=request.user)
        newsletters_form = NewslettersForm(instance=profile_user)

        return render(request, 'authorization/user_page.html', {
            'profile_user': profile_user,
            'avatar_form': avatar_form,
            'info_form': info_form,
            'newsletters_form': newsletters_form,
        } | base_ctx)
