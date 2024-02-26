import django_filters

from .models import *


class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ['title', 'gender', 'phone','profession', 'organization', 
                   'address', 'bio', 'date_created', 'user']


class AbstractFilter(django_filters.FilterSet):
    class Meta:
        model = Abstract
        fields = '__all__'
        exclude = ['topics', 'abstract_body', 'author_name', 'author_email',
                   'author_affiliation', 'presenter_name', 'presenter_email',
                   'date_created', 'presentation_preference', 'author', 'keywords',
                   'status', 'upload', 'date_updated']