from django.shortcuts import render

# Create your views here.
def index(request):
	if request.method == 'POST':
		print(request.POST.dict())
	return render(request, 'testroom.html')