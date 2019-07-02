from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.uploadhandler import FileUploadHandler
from django.db.models import Q




from image_uploader.models import UploadedFile
from products.forms import UploadFileForm
def handle_upload(request):
	if request.is_ajax():
		form = UploadFileForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form_id = request.POST.get('form_id')
			qq_file_id = int(request.POST.get('qq-file-id'))
			images = request.FILES.getlist('image')
			lookups_images=(Q(form_id__iexact='form_id'))
			for x in images:
				temporary_file = UploadedFile.objects.create(uploaded_file=x, form_id=form_id, file_id=qq_file_id)
				lookups_images=lookups_images|(Q(file_id=qq_file_id))
				qq_file_id += 1
			uploaded_qs = UploadedFile.objects.filter(form_id = form_id).filter(lookups_images)
			all_files = (len(UploadedFile.objects.filter(form_id = form_id)))
			images = [{
					"image_url": uploaded_obj.thumbnail.url,
					} 
			for uploaded_obj in uploaded_qs]
			json_data = {
					'image': images,
					'count':all_files
					}
			return JsonResponse(json_data)
		else:
			print(form.errors)
	return HttpResponse('html')

def handle_delete(request):
	if request.is_ajax():
		id_ = request.POST.get('data')
		if str(id_) == 'delete_on_reload':
			form_id = request.POST.get('form_id')
			files = UploadedFile.objects.filter(form_id=form_id)
			for x in files:
				x.uploaded_file.delete()
				x.thumbnail.delete()
				x.delete()
		else:
			form_id = request.POST.get('form_id')
			file = UploadedFile.objects.get(file_id=id_,form_id=form_id)
			file.uploaded_file.delete()
			file.thumbnail.delete()
			file.delete()
			all_files = len(UploadedFile.objects.filter(form_id = form_id))
			json_data = {
						'count':all_files
						}
			return JsonResponse(json_data)
	return HttpResponse('html')

def handle_rotate(request):
	if request.is_ajax():
		id_ = request.POST.get('data')
		form_id = request.POST.get('form_id')
		file = UploadedFile.objects.get(file_id=id_,form_id=form_id)
		UploadedFile.objects.rotate_image(image=file)
		json_data = {
					'image_url':file.thumbnail.url
					}
		return JsonResponse(json_data)
	return HttpResponse('html')





