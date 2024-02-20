from django.db import models

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
    title = models.CharField(max_length=50, choices=TITLE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profession = models.CharField(max_length=200, null=True)
    organization = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=300, null=True)
    bio = models.CharField(max_length=600, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name, self.last_name, self.email, self.date_created
    

class Event_topics(models.Model):
    topics = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.topic

class Presentation_type(models.Model):
    presentation_preference = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.presentation_preference    

class Abstract_form(models.Model):
    title = models.CharField(max_length=200, null=True)
    abstract_body = models.CharField(max_length=600, null=True)
    keywords = models.CharField(max_length=300, null=True)
    author_name = models.CharField(max_length=200, null=True)
    author_email = models.CharField(max_length=200, null=True)
    author_affiliation = models.CharField(max_length=200, null=True)
    presenter_name = models.CharField(max_length=200, null=True)
    presenter_email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    topics = models.ManyToManyField(Event_topics)
    presentation_preference = models.ManyToManyField(Presentation_type)

    def __str__(self):
        return self.title, self.topics, self.presentation_preference, self.date_created

class Abstract_status(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Under Review", "Under Review"),
        ("Accepted", "Accepted"),
        ("Rejected.", "Rejected"),
    )
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    abstract_form = models.ForeignKey(Abstract_form, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.author, self.status, self.date_created



