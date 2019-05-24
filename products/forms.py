from django.http import JsonResponse
from django import forms


from django_file_form.forms import MultipleUploadedFileField, FileFormMixin


from .models import Product, Image
from categories.models import Size




class ProductCreateForm(FileFormMixin, forms.ModelForm):
	class Meta:
		model = Product
		fields = [
		'title',
		'description',
		'price',
		'brand',
		'sex',
		'category',
		'size',
			]
	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(ProductCreateForm, self).__init__(*args, **kwargs)	

	def clean_category(self):
		request = self.request
		data = self.cleaned_data
		if data.get('category') == 'select a category':
			self.add_error('category', 'Please, select a category')
		return data.get('category')



class ImageForm(ProductCreateForm):
	image = MultipleUploadedFileField()
	def clean_image(self):
		data = self.cleaned_data
		image = data.get('image')
		for img in image:
			img_ = str(img)
			filename, ext = img_.rsplit('.', 1)
			if ext != 'jpg': 
				raise forms.ValidationError('Not')
		return image

	def save(self, commit=True):
		product = super(ProductCreateForm, self).save(commit=False)
		product.user = self.request.user
		product.active = True
		if commit:
			product.save()
		for idx, file in enumerate(self.cleaned_data['image']):
			print(file)
			Image.objects.create(
				product=product,
				image=file,
				slug=product.slug,
				image_order=idx+1
								)
		self.delete_temporary_files()
		return product
		


class ProductUpdateForm(ProductCreateForm):
	def __init__(self, request, slug, *args, **kwargs):
		super(ProductUpdateForm, self).__init__(request, *args, **kwargs)
		product = Product.objects.get(slug=slug)
		category = product.category
		size = Size.objects.filter(size_for__icontains=category)
		self.fields['size'].queryset = size
		def get_upload_url(self):
			return reverse('products:example_handle_upload')














