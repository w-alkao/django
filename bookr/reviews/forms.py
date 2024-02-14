from django import forms
from .models import Publisher


SEARCH_CHOICES = (
  ("title", "Title"),
  ("contributor", "Contributor")
)
class SearchForm(forms.Form):
  search = forms.CharField(required=False, min_length=3)
  search_in = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)



#------------------------------------------------------------------------------------



class PublisherForm(forms.ModelForm):
  class Meta:
    model = Publisher
    fields = "__all__"