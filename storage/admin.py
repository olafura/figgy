'''
Admin module for Books
'''

from django.contrib import admin

from storage.models import Book, Alias


class InlineAliasAdmin(admin.StackedInline):
    '''Have Aliases show up under Books'''
    model = Alias
    extra = 0


class BookAdmin(admin.ModelAdmin):
    '''Basic Book Admin with Aliases shown'''
    inlines = [InlineAliasAdmin]

    list_display = ['id', 'title', 'list_aliases']

    def list_aliases(self, obj):
        '''Formats aliases for showing'''
        if obj:
            return '<pre>%s</pre>' % '\n'.join(
                     [o.value for o in obj.aliases.all()])

    list_aliases.allow_tags = True

admin.site.register(Book, BookAdmin)

