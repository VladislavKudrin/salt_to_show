from django import forms

from .models import Order


# class OrderCompletedForm(forms.ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = [
# 			'order_id',
# 			'status',
# 			'total'
# 				]
# 	def __init__(self, request, *args, **kwargs):
# 		super(ProductCreateForm, self).__init__(*args, **kwargs)
# 		self.request = request
# 		