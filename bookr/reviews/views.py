from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from django.contrib import messages
from django.utils import timezone
from PIL import Image
from django.contrib.auth.decorators import user_passes_test, login_required
from io import BytesIO
from django.core.files.images import ImageFile
from django.core.exceptions import PermissionDenied



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
  
  if request.user.is_authenticated:
    max_viewed_books_length = 10
    viewed_books = request.session.get('viewed_books', [])
    viewed_book = [book.id, book.title]
    if viewed_book in viewed_books:
      viewed_books.pop(viewed_books.index(viewed_book))
    viewed_books.insert(0, viewed_book)
    viewed_books = viewed_books[:max_viewed_books_length]
    request.session['viewed_books'] = viewed_books
    
  return render(request,'reviews/book_detail.html', context)


#------------------------------------------------------------------------------


def book_search(request):
  search_text = request.GET.get("search", "")
  form = SearchForm(request.GET)
  books = set()
  search_history = request.session.get("search_history", [])
  
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
          
    if request.user.is_authenticated:
      search_his = [search, search_by]
      if search_his in search_history:
        search_history.pop(search_history.index(search_his))
      search_history.insert(0, search_his)
      request.session['search_history'] = search_history
  elif search_history:
    initial = dict(search=search_text, search_in=search_history[-1][0])
    form = SearchForm(initial=initial)

  context = {
    "form": form,
    "search_text": search_text,
    "books": books,
  }

  return render(request, "reviews/search_result.html", context)



#--------------------------------------------------------------------------------------------------------



def is_staff_user(user):
  return user.is_staff

@user_passes_test(is_staff_user)
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

  context = {"instance": publisher, "form": form, "model_type": "Publisher"}
  return render(request, "reviews/instance_form.html", context)



#-------------------------------------------------------------------------------------------------------


@login_required
def review_edit(request, b_pk, r_pk=None):
  book = get_object_or_404(Book, pk=b_pk)
  if r_pk:
    review = get_object_or_404(Review, book_id=b_pk, pk=r_pk)
    user = request.user
    if not user.is_staff and review.creator.id != user.id:
      raise PermissionDenied
  else:
    review = None

  if request.method == "POST":
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
      updated_review = form.save(False)
      updated_review.book = book
      if review:
        updated_review.date_edited = timezone.now()
        messages.success(request, f"Review for {book} updated.")
      else:
        messages.success(request, f"Review for {book} created.")

      updated_review.save()
      return redirect("book_detail", book.pk)
  else:
    form = ReviewForm(instance=review)

  context = {
    "form": form,
    "instance": review,
    "model_type": "Review",
    "related_instance": book,
    "related_model_type": "Book"
  }

  return render(request, "reviews/review_form.html", context)



#-------------------------------------------------------------------------------------------


@login_required
def book_media(request, pk):
  book = get_object_or_404(Book, pk=pk)
  if request.method == "POST":
    form = BookMediaForm(request.POST, request.FILES, instance=book)
    if form.is_valid():
      book = form.save(False)
      cover = form.cleaned_data.get("cover")
      if cover:
        image = Image.open(cover)
        image.thumbnail((300, 300))
        image_data = BytesIO()
        image.save(fp=image_data, format=cover.image.format)
        image_file = ImageFile(image_data)
        book.cover.save(cover.name, image_file)
      book.save()
      messages.success(request, f"Book {book} was successfully updated.")
      return redirect("book_detail", book.pk)
  else:
    form = BookMediaForm(instance=book)
    
  context = {
    "form": form,
    "instance": book,
    "model_type": "Book",
    "is_file_upload": True
  }
  
  return render(request, "reviews/file_form.html", context)