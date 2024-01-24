from django.contrib import admin
from reviews.models import Publisher, Contributor, Book, BookContributor, Review

# Register your models here

class BookAdmin(admin.ModelAdmin):
  date_hierarchy = 'publication_date'
  list_display = ('title', 'isbn13', 'has_isbn')
  list_filter = ('publisher', 'publication_date')
  search_fields = ('title', 'isbn', 'publisher__name')
  @admin.display(
    ordering='isbn',
    description='ISBN-13',
    empty_value='-/',
  )
  def isbn13(self, obj):
    return f'{obj.isbn[0:3]}-{obj.isbn[3:4]}-{obj.isbn[4:6]}-{obj.isbn[6:12]}-{obj.isbn[12:13]}'

  @admin.display(
    boolean=True,
    description='Has ISBN-13'
  )
  def has_isbn(self, obj):
    return bool(obj.isbn)


class ContributorAdmin(admin.ModelAdmin):
  list_display = ('last_names', 'first_names',)
  search_fields = ('last_names', 'first_names')
  list_filter = ('last_names',)


class ReviewAdmin(admin.ModelAdmin):
  exclude = ('date_edited',)
  #fields = ('content', 'rating', 'creator', 'book')
  fieldsets = (
    (None, {'fields': ('creator', 'book')}),
    ('Review content', {'fields': ('content', 'rating')})
  )

admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)