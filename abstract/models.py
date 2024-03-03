from django.db import models
from django.contrib.auth.models import User, Group
import secrets
from .paystack import Paystack


# Create your models here.

class Author(models.Model):
    """
    Model representing an author of an abstract submission.
    """
    TITLE = (
        ("Mr.", "Mr."),
        ("Mrs", "Mrs."),
        ("Dr.", "Dr."),
        ("Prof.", "Prof."),
    )
    GENDER = (
       ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, choices=TITLE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    profession = models.CharField(max_length=200, null=True)
    organization = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=300, null=True)
    bio = models.TextField(max_length=600, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name} - {self.email} - {self.phone}'


class Topic(models.Model):
    """
    Model representing a topic for an abstract submission.
    """    
    topics = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.topics

class Presentation_type(models.Model):
    """
    Model representing a preferred presentation type for an abstract submission.
    """
    presentation_preference = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.presentation_preference
    

    
class Event(models.Model):
    """
    Model representing an event for which abstracts can be submitted.
    """
    event = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.event
    

class Editor(models.Model):
    """
    Model representing an editor associated with a group for abstract review.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'
    


class Abstract(models.Model):
    """
    Model representing an abstract submission for an event.
    """
    STATUS = (
        ("Pending", "Pending"),
        ("Under Review", "Under Review"),
        ("Accepted", "Accepted"),
        ("Rejected.", "Rejected"),
    )
    title = models.CharField(max_length=200, null=True)
    abstract_body = models.TextField(max_length=600, null=True)
    keywords = models.CharField(max_length=300, null=True)
    author_name = models.CharField(max_length=200, null=True)
    author_email = models.EmailField(max_length=200, null=True)
    author_affiliation = models.CharField(max_length=200, null=True)
    presenter_name = models.CharField(max_length=200, null=True)
    presenter_email = models.EmailField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateField(auto_now=True, null=True)
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending', blank=True)
    topics = models.ManyToManyField(Topic)
    presentation_preference = models.ManyToManyField(Presentation_type)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, blank=True)
    editors = models.ManyToManyField(Group, related_name='assigned_abstracts', blank=True)
    def __str__(self):
        return f'{self.title} - {self.author_name} - {self.presentation_preference} - {self.presenter_name}'
    

class Contact(models.Model):    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    message = models.TextField(max_length=600)

    def __str__(self):
        return f'{self.first_name} - {self.last_name} - {self.email} - {self.phone}'
    

class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.name


class PlaceOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    # item_amount = models.PositiveIntegerField(default=1)
    total_cost = models.PositiveIntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.user} - {self.product}'
    


class Payment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()
	ref = models.CharField(max_length=200)
	email = models.EmailField()
	verified = models.BooleanField(default= False)
	date_time = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.user} - {self.amount}'


	def save(self, *args, **kwarges):
		while not self.ref:
			ref = secrets.token_urlsafe(50)
			object_with_similar_ref = Payment.objects.filter(ref=ref)
			if not object_with_similar_ref:
				self.ref=ref

		super().save(*args, **kwarges)


	def amount_value(self):
		return int(self.amount) * 100


	def verify_payment(self):
		paystack = Paystack()
		status, result = paystack.verify_payment(self.ref, self.amount)
		if status:
			if result['amount'] / 100 == self.amount:
				self.verified = True
				self.save()

			if self.verified:
				return True
			else:
				return False