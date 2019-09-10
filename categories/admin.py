from django.contrib import admin

from .models import Size, Brand, Undercategory, Category, Gender, Overcategory, Condition

class Undercategory_tab(admin.TabularInline):
	model = Undercategory

class Category_tab(admin.TabularInline):
	model = Category

class Gender_tab(admin.TabularInline):
	model = Gender



class SizeAdmin(admin.ModelAdmin):
	list_display = ['size', 'size_for', 'size_type']
	class Meta:
		model=Size

class UndercategoryAdmin(admin.ModelAdmin):
	list_display = ['undercategory_admin', 'undercategory_for']
	class Meta:
		model=Undercategory

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['category_admin', 'category_for']
	inlines = [Undercategory_tab]
	class Meta:
		model=Category

class GenderAdmin(admin.ModelAdmin):
	list_display = ['gender_admin', 'gender_for']
	inlines = [Category_tab]
	class Meta:
		model=Gender

class OvercategoryAdmin(admin.ModelAdmin):
	inlines = [Gender_tab]
	class Meta:
		model=Overcategory

admin.site.register(Size, SizeAdmin)
admin.site.register(Undercategory, UndercategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Overcategory, OvercategoryAdmin)


admin.site.register(Brand)
admin.site.register(Condition)








