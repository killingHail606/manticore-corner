from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(max_length=1000, label='Добавить новый комментарий', widget=forms.Textarea(attrs={'id': 'new_comment'}))


class SearchForm(forms.Form):
    body = forms.CharField(max_length=300, label='', widget=forms.TextInput(attrs={'placeholder': 'Введите запрос...'}))

