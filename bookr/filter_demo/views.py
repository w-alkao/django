from django.shortcuts import render

# Create your views here.
def index(request):
	names = "john,doe,mark,swain"
	context = {
		'names': names
	}
	
	return render(request, "index.html", context)



def greeting_view(request):
	context = {
		'username': 'jdoe'
	}
	
	return render(request, "simple_tag_template.html", context)