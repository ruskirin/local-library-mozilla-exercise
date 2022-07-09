from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


admin.site.register(Genre)
admin.site.register(Language)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'instance_id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Summary', {
            'fields': ('book', 'imprint', 'instance_id')
        }),
        ('Availability', {
            'fields': ('status', 'borrower', 'due_back')
        })
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'dob', 'dod')
