from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
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
        return self.first_name
    


class Topic(models.Model):
    topics = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.topics

class Presentation_type(models.Model):
    presentation_preference = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.presentation_preference    

class Abstract(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Under Review", "Under Review"),
        ("Accepted", "Accepted"),
        ("Rejected.", "Rejected"),
    )
    title = models.CharField(max_length=200, null=True)
    abstract_body = models.TextField(max_length=600, null=True, blank=True)
    keywords = models.CharField(max_length=300, null=True)
    author_name = models.CharField(max_length=200, null=True)
    author_email = models.EmailField(max_length=200, null=True)
    author_affiliation = models.CharField(max_length=200, null=True)
    presenter_name = models.CharField(max_length=200, null=True)
    presenter_email = models.EmailField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateField(auto_now=True, null=True)
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    topics = models.ManyToManyField(Topic)
    presentation_preference = models.ManyToManyField(Presentation_type)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    

class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    message = models.TextField(max_length=600)

    def __str__(self):
        return self.first_name, self.first_name, self.email, self.phone
