from django.shortcuts import render
from django.http import HttpResponse



from products.forms import ImageForm
def handle_upload(request):
	print('hi')
	if request.is_ajax():
		print('ajax')
		print(request.FILES)
		form = ImageForm(request.FILES)
		if form.is_valid():
			print('valid')
		else:
			print('invalid')
	return HttpResponse('html')

