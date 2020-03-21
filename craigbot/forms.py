from django import forms
from .models import newBotRequest

# Request object is created to temporarily store info
# This way we can search craigslist accordingly before inserting
# into database
class newBotRequestForm(forms.ModelForm):

    class Meta:
        model = newBotRequest
        fields = ('city', 'category', 'search_query', 'price_min', 'price_max',)
