from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Author

def author_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='author')
		instance.groups.add(group)
		Author.objects.create(
			user=instance,
			first_name=instance.username,
			)
		print('Profile created!')

post_save.connect(author_profile, sender=User)