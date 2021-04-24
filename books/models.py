from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models.signals import post_save
from django.dispatch import receiver

from authorization.models import Profile


class BooksSection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:books_section', args=[self.slug])


class BooksGenre(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    list = models.ForeignKey(BooksSection, related_name='genres', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.list.title} - {self.title}'

    def get_absolute_url(self):
        return reverse('books:books_genre', args=[self.list.slug, self.slug])


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=150)
    book_cover = models.ImageField(upload_to='books/%Y/%m/%d')
    number_of_pages = models.IntegerField()
    year_publishing = models.IntegerField()
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    retelling = models.TextField(blank=True)
    quotes = models.TextField(blank=True)
    list_of = models.ForeignKey(BooksSection, related_name='books', on_delete=models.PROTECT)
    genre = models.ForeignKey(BooksGenre, related_name='books', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=250)
    date_pub = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date_pub',)

    def __str__(self):
        return f'{self.author} - {self.title}'

    def get_absolute_url(self):
        return reverse('books:book_detail', args=[self.slug])


@receiver(post_save, sender=Book)
def my_callback(sender, **kwargs):
    model = kwargs['instance']
    if model.list_of.id == 3 and kwargs['created'] == True:
        users = User.objects.all()

        subject = 'Новая рекомендуемая книга'
        from_email = 'manticore.thoughts@gmail.com'

        for user in users:
            try:
                profile_user = Profile.objects.get(user=user)
                if profile_user.email_newsletters:
                    username = user.username
                    email = user.email

                    html_message = render_to_string('email/new_recom_book.html', {'book_title': model.title,
                                                                                  'book_author': model.author,
                                                                                  'book_picture': model.book_cover,
                                                                                  'book_description': model.description,
                                                                                  'book_link': reverse('books:book_detail',
                                                                                                       args=[model.slug]),
                                                                                  'user_username': username
                                                                                  })
                    plain_message = strip_tags(html_message)
                    mail.send_mail(subject, plain_message, from_email, [email], html_message=html_message)
            except:
                continue
