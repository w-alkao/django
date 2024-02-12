from django.shortcuts import render
from .forms import ExampleForm, OrderForm

# Create your views here.

def html_form_example(request):
  for name in request.POST:
    print(f"{name}: {request.POST.getlist(name)}")

  return render(request, "html_form_example.html", {"method": request.method})



def django_form_example(request):
  if request.method == "POST":
    form = ExampleForm(request.POST)
    if form.is_valid():
      for name, value in form.cleaned_data.items():
        print(f"{name}: ({type(value)}) {value}")
  else:
    form = ExampleForm()

  context = {
    "method": request.method,
    "form": form
  }

  return render(request, "django_form_example.html", context)


initial = {"email": "user@example.com"}
def order_form(request):
  if request.method == "POST":
    form = OrderForm(request.POST, initial=initial)
    if form.is_valid():
      for name, value in form.cleaned_data.items():
        print(f'{name}: ({type(value)}) {value}')
  else:
    form = OrderForm(initial=initial)

  context = {
    "method": request.method,
    "form": form
  }

  return render(request, "order_form.html", context)