from django import forms
from .models import Publisher, Review, Book


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



#--------------------------------------------------------------------------------


class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    exclude = ("book", "date_edited")

  rating = forms.IntegerField(min_value=0, max_value=5)
  
  
#-----------------------------------------------------------------------------------------


class BookMediaForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ["cover", "sample"]
    