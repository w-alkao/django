from django.shortcuts import render

# Create your views here.

def form_example(request):
  for name in request.POST:
    print(f"{name}: {request.POST.getlist(name)}")

  return render(request, "form-example.html", {"method": request.method})