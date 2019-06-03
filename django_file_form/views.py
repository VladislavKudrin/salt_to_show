from django.http import HttpResponse, HttpResponseNotFound
from django.views import generic

from .models import UploadedFile
from .uploader import FileFormUploader
from .util import check_permission


handle_upload = FileFormUploader()


class DeleteFile(generic.View):
    def post(self, request, file_id=None):
        file_id = file_id or request.POST.get('qquuid')

        return self.delete_file(request, file_id)

    def delete(self, request, file_id):
        return self.delete_file(request, file_id)

    def delete_file(self, request, file_id):
        check_permission(request)

        uploaded_file = UploadedFile.objects.try_get(file_id=file_id)
        if uploaded_file:
            uploaded_file.delete()
            return HttpResponse("ok")
        else:
            return HttpResponseNotFound()
