from django.db import models


class Rules(models.Model):
    title = models.CharField(max_length=100)
    rules_of_section = models.TextField()

    def __str__(self):
        return self.title
