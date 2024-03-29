import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateResponseMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from django.contrib.sitemaps import Sitemap

from taggit.models import Tag

from authorization.models import Profile
from .models import Post, AboutBlog, Comment
from books.models import Book
from wall_of_heroes.models import Hero
from .functions import get_random_posts, lexicon, quote
from .forms import CommentForm, SearchForm


class MainPage(TemplateResponseMixin, View):

    template_name = 'blog/home.html'

    def get(self, request):
        last_posts = Post.objects.filter(status='published').order_by('-date_pub')[:4]
        random_posts = get_random_posts(last_posts)[:4]

        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        ctx = {'section': 'home',
               'random_posts': random_posts,
               'last_posts': last_posts,
               } | base_ctx
        return self.render_to_response(ctx)


class Articles(TemplateResponseMixin, View):
    template_name = 'blog/articles.html'

    def get(self, request, slug=None):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }
        if slug is None:
            posts = Post.objects.filter(status='published')
            section = 'articles'
        else:
            if slug == "":
                posts = Post.objects.filter(status='published')
            else:
                tag_posts = get_object_or_404(Tag, slug=slug)
                posts = Post.objects.filter(status='published', tags=tag_posts)
                section = None

        all_tags = Tag.objects.all()
        paginator = Paginator(posts, 6)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        ctx = {'section': section,
               'posts': posts,
               'all_tags': all_tags,
               } | base_ctx
        return self.render_to_response(ctx)


class PostDetailView(TemplateResponseMixin, View):
    template_name = 'blog/article/detail.html'

    def get(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        profiles = Profile.objects.all()

        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        post.views += 1
        post.save()
        comment_form = CommentForm()

        try:
            last_id = int(list(Comment.objects.all().order_by('number_comment'))[-1].number_comment)
        except IndexError:
            last_id = 0
        print(last_id)
        ctx = {'post': post,
               'comment_form': comment_form,
               'profiles': profiles,
               'last_id': last_id,
               } | base_ctx
        return self.render_to_response(ctx)


class SearchView(TemplateResponseMixin, View):
    template_name = 'blog/search.html'

    def post(self, request):
        search_request = request.POST['body']

        posts = Post.objects.filter(
            Q(title__icontains=search_request) | Q(body__icontains=search_request)
        )

        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        print(search_request)
        ctx = {
            'posts': posts,
        } | base_ctx
        return self.render_to_response(ctx)

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        return self.render_to_response(context=base_ctx)


class AboutBlogView(TemplateResponseMixin, View):
    template_name = 'blog/about_blog.html'

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }
        if len(AboutBlog.objects.all()) > 0:
            about_blog = AboutBlog.objects.all()[0]
        else:
            about_blog = ''
        ctx = {'section': 'about_blog',
               'about_blog': about_blog,
               } | base_ctx
        return self.render_to_response(ctx)


class PrivacyView(TemplateResponseMixin, View):
    template_name = 'blog/privacy.html'

    def get(self, request):
        base_ctx = {
            'lexicon': lexicon(),
            'quote': quote(),
            'search_form': SearchForm(),
        }

        return self.render_to_response(base_ctx)


@login_required
@require_POST
def post_comment(request):
    post_id = request.POST['id']
    text_of_comment = request.POST['text_of_comment']
    num_comments = int(request.POST['num_comments'])
    answer_num = request.POST['answer_num']

    try:
        last_id = int(list(Comment.objects.all().order_by('number_comment'))[-1].number_comment)
    except IndexError:
        last_id = 0
    print(last_id)

    if answer_num != 'false':
        username = text_of_comment.split(',')[0]
        reply_to = f'<span class="reply_nick" onclick="go_to_comment(\'{str(answer_num)}\')">{username}</span>'
        text_of_comment = text_of_comment[len(username):]
        comment = Comment.objects.create(user=request.user, body=text_of_comment,
                                         reply_to=reply_to, number_comment=last_id+1)
    else:
        comment = Comment.objects.create(user=request.user, body=text_of_comment, number_comment=last_id+1)

    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            post.comments.add(comment)
            post.comments.remove()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


def handler404(request, *args, **kwargs):
    base_ctx = {
        'lexicon': lexicon(),
        'quote': quote(),
        'search_form': SearchForm(),
    }

    return render(request, 'errors/404.html', base_ctx, status=404)


def handler500(request, *args, **kwargs):
    base_ctx = {
        'lexicon': lexicon(),
        'quote': quote(),
        'search_form': SearchForm(),
    }

    return render(request, 'errors/500.html', base_ctx, status=500)


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return ['blog:main_blog', 'blog:articles', 'blog:about_blog']

    def location(self, item):
        return reverse(item)


class WallRulesSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['my_rules:my_rules', 'wall_of_heroes:heroes']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_pub


class BooksSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Book.objects.filter()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_pub


class HeroesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Hero.objects.filter()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_pub