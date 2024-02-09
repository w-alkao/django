from django.shortcuts import render, get_object_or_404
from .models import Book, Contributor
from .utils import average_rating
from .forms import SearchForm



# Create your views here.

def welcome_view(request):
  return render(
    request,
    'base.html'
  )


#------------------------------------------------------------------------------


def book_list(request):
  books = Book.objects.all()
  book_list = []
  for book in books:
    reviews = book.review_set.all()
    if reviews:
      book_rating = average_rating([review.rating for review in reviews])
      number_of_reviews = len(reviews)
    else:
      book_rating = None
      number_of_reviews = 0
    book_list.append({
      'book': book,
      'book_rating': book_rating,
      'number_of_reviews': number_of_reviews,
    })
  context = {
    'book_list': book_list,
  }
  return render(
    request,
    'reviews/book_list.html',
    context
  )


#---------------------------------------------------------------------------


def book_detail(request, pk):
  book = get_object_or_404(Book, pk=pk)
  reviews = book.review_set.all()

  if reviews:
    book_rating = average_rating([review.rating for review in reviews])
    context = {
      'book': book,
      'book_rating': book_rating,
      'reviews': reviews,
    }
  else:
    context = {
      'book': book,
      'book_rating': None,
      'reviews': None
    }

  return render(
    request,
    'reviews/book_detail.html',
    context
  )


#------------------------------------------------------------------------------

def book_search(request):
  if request.method == "GET":
    form = SearchForm(request.GET)
    book_list = []
    search_text = request.GET.get("search")
    if form.is_valid() and search_text is not None:
      search_by = form.cleaned_data.get("search_in")
      if search_by == "title":
        books = Book.objects.filter(title__icontains=search_text)
        for book in books:
          book_list.append({"book": book})
      elif search_by == "contributor":
        contributor1 = Contributor.objects.filter(first_names=search_text)
        contributor2 = Contributor.objects.filter(last_names=search_text)
        for contributor in contributor1:
          books = contributor.book_set.all()
          for book in books:
            book_list.append({"book": book})

        for contributor in contributor2:
          books = contributor.book_set.all()
          for book in books:
            book_list.append({"book": book})

      else:
        book_list = []


  else:
    form = SearchForm()

  context = {
    "book_list": book_list,
    "form": form,
    "search_text": search_text
  }

  return render(request, "reviews/search_result.html", context)

