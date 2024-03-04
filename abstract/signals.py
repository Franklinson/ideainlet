from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Author

def author_profile(sender, instance, created, **kwargs):
	"""
    Creates an author profile whenever a new user is saved.

    Args:
        sender (type): The model class that sent the signal.
        instance (User): The specific User instance that was saved.
        created (bool): A boolean indicating whether the User instance was created or updated.
        **kwargs: Additional keyword arguments passed to the signal.
    """
	if created:
		group = Group.objects.get(name='author')
		instance.groups.add(group)
		Author.objects.create(
			user=instance,
			first_name=instance.username,
			)
		print('Profile created!')

post_save.connect(author_profile, sender=User)