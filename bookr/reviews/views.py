from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Contributor, Publisher
from .utils import average_rating
from .forms import SearchForm, PublisherForm
from django.contrib import messages



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
  search_text = request.GET.get("search", "")
  form = SearchForm(request.GET)
  books = set()

  if form.is_valid() and form.cleaned_data["search"]:
    search = form.cleaned_data["search"]
    search_by = form.cleaned_data.get("search_in") or "title"
    if search_by == "title":
      books = Book.objects.filter(title__icontains=search)
    else:
      contributor_first_name = Contributor.objects.filter(first_names__icontains=search)
      contributor_last_name = Contributor.objects.filter(last_names__icontains=search)
      for contributor in contributor_first_name:
        for book in contributor.book_set.all():
          books.add(book)
      for contributor in contributor_last_name:
        for book in contributor.book_set.all():
          books.add(book)

  context = {
    "form": form,
    "search_text": search_text,
    "books": books,
  }

  return render(request, "reviews/search_result.html", context)



#--------------------------------------------------------------------------------------------------------



def publisher_edit(request, pk=None):
  if pk is not None:
    publisher = get_object_or_404(Publisher, pk=pk)
  else:
    publisher = None

  if request.method == "POST":
    form = PublisherForm(request.POST, instance=publisher)
    if form.is_valid():
      updated_publisher = form.save()
      if publisher is None:
        messages.success(request, f"Publisher {updated_publisher} was created.")
      else:
        messages.success(request, f"Publisher {updated_publisher} was updated")
      return redirect("publisher_edit", updated_publisher.pk)
  else:
    form = PublisherForm(instance=publisher)

  context = {"method": request.method, "form": form}
  return render(request, "reviews/publisher_form.html", context)
