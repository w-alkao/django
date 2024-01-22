from django.contrib.admin import AdminSite

class Comment8orAdminSite(AdminSite):
  title_header = 'c8 site admin'
  site_header = 'c8admin'
  index_title = 'c8admin'
  logout_template = 'templates/comment8or/logged_out.html'