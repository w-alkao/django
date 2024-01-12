from django.shortcuts import render

# Create your views here.

def index(request):
  welcome_message = "Welcome to Bookr"

  return render(
    request,
    "base.html",
    {"welcome_message": welcome_message}
  )


def search_view(request):
  search_text = request.GET.get("q") or "..."

  return render(
    request,
    "search_result.html",
    {"search_text": search_text}
  )