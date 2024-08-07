from django.shortcuts import render
from .forms import ExampleForm, OrderForm, FileUploadForm, FileUploadForm2, UploadForm, ImageUploadForm
from django.conf import settings
import os
from PIL import Image
from .models import ExampleModel

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



def media_html_form(request):
  if request.method == "POST":
    save_path = settings.MEDIA_ROOT / request.FILES["file_upload"].name
    with open(save_path, "wb") as output_file:
      for chunk in request.FILES["file_upload"].chunks():
        output_file.write(chunk)
  return render(request, "media_html_form.html")


def media_django_form(request):
  if request.method == "POST":
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["file_upload"].name)
      with open(save_path, "wb") as output_file:
        #for chunk in request.FILES["file_upload"].chunks(): we can use this too
        for chunk in form.cleaned_data["file_upload"].chunks():
          output_file.write(chunk)
  else:
    form = UploadForm()

  context = {
    "form": form
  }

  return render(request, "media_django_form.html", context)


def image_django_form(request):
  if request.method == "POST":
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["image_upload"].name)
      image = Image.open(form.cleaned_data["image_upload"])
      image.thumbnail((50, 50))
      image.save(save_path)
  else:
    form = ImageUploadForm()

  context = {
    "form": form
  }

  return render(request, 'image_django_form.html', context)


def media_example(request):
  instance = None
  if request.method == "POST":
    form = FileUploadForm(request.POST, request.FILES)
    if form.is_valid():
      instance = ExampleModel()
      instance.image_field = form.cleaned_data["image_upload"]
      instance.file_field = form.cleaned_data["file_upload"]
      instance.save()
  else:
    form = FileUploadForm()

  context = {
    "form": form,
    "instance": instance,
  }

  return render(request, "media_example.html", context)



def media_example2(request):
  instance = None
  if request.method == "POST":
    form = FileUploadForm2(request.POST, request.FILES)
    if form.is_valid():
      instance = form.save()
  else:
    form = FileUploadForm()

  context = {
    "form": form,
    "instance": instance,
  }

  return render(request, "media_example2.html", context)
