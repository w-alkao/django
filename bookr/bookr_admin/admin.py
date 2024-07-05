from django.contrib import admin


# Register your models here.
class BookrAdmin(admin.AdminSite):
	site_header = "Bookr Administration"
	logout_template = 'admin/logout.html'
	
