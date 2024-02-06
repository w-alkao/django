from django import forms


SEARCH_CHOICES = (
  ("title", "Title"),
  ("contributor", "Contributor")
)
class SearchForm(forms.Form):
  search = forms.CharField(required=False, min_length=3)
  search_in = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)