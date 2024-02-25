from django.contrib import admin
from .models import Author, Abstract, Topic, Presentation_type

# Register your models here.

admin.site.register(Author)
admin.site.register(Topic)
admin.site.register(Presentation_type)
admin.site.register(Abstract)
