from django.forms import ModelForm
from .models import Abstract


class AbstractForm(ModelForm):
    class Meta:
        model = Abstract
        fields = '__all__'