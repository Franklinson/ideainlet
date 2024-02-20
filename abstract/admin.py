from django.contrib import admin
from .models import Author, Abstract_form, Abstract_status, Event_topics, Presentation_type

# Register your models here.

admin.site.register(Author)
admin.site.register(Event_topics)
admin.site.register(Presentation_type)
admin.site.register(Abstract_form)
admin.site.register(Abstract_status)
