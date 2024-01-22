from django.contrib.admin import AdminSite


# Register your models here.
class BookrAdminSite(AdminSite):
  title_header = 'Bookr Admin'
  site_header = 'Bookr administration'
  index_title = 'Bookr site admin'

