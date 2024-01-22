from django.contrib import admin
from reviews.models import Publisher, Contributor, Book, BookContributor, Review

# Register your models here

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'isbn13')
  def isbn13(self, obj):
    return f'{obj.isbn[0:3]}-{obj.isbn[3:4]}-{obj.isbn[4:6]}-{obj.isbn[6:12]}-{obj.isbn[12:13]}'


def initialled_name(obj):
  initials = ''.join([name[0] for name in obj.first_names.split(' ')])
  return f'{obj.last_names}, {initials}'

class ContributorAdmin(admin.ModelAdmin):
  list_display = (initialled_name,)

admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)