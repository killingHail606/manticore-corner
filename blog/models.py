from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from authorization.models import Profile


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE, unique=False)
    body = models.CharField(max_length=1000)
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_pub',)

    def __str__(self):
        return self.body


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=250)
    date_pub = models.DateTimeField(auto_now_add=True)
    body = HTMLField(blank=True)
    main_photo = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    tags = TaggableManager(blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='post_liked',
                                        blank=True)
    comments = models.ManyToManyField(Comment, related_name='post_comments', blank=True)
    views = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ('-date_pub',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def total_likes(self):
        return self.likes.count()


class Lexicon(models.Model):
    word = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=110)

    def __str__(self):
        return self.word


class Quote(models.Model):
    body = models.TextField(max_length=250)
    author = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.author} сказал: "{self.body}"'


class AboutBlog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    picture = models.ImageField(upload_to='about_blog/')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def my_callback(sender, **kwargs):
    model = kwargs['instance']
    if model.status == 'published' and kwargs['created'] == True:
        users = User.objects.all()

        subject = 'Новый пост в блоге'
        from_email = 'manticore.thoughts@gmail.com'

        for user in users:
            try:
                profile_user = Profile.objects.get(user=user)
                if profile_user.email_newsletters:
                    username = user.username
                    email = user.email

                    html_message = render_to_string('email/new_post.html', {'post_title': model.title,
                                                                            'post_picture': model.main_photo,
                                                                            'post_body': model.body,
                                                                            'post_link': reverse('blog:post_detail', args=[model.slug]),
                                                                            'user_username': username
                                                                            })
                    plain_message = strip_tags(html_message)
                    mail.send_mail(subject, plain_message, from_email, [email], html_message=html_message)
            except:
                continue
