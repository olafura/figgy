# encoding: utf-8
'''Models for Books'''

from django.db import models


class BaseModel(models.Model):
    '''Base class for all models'''
    created_time = models.DateTimeField('date created', auto_now_add=True)
    last_modified_time = models.DateTimeField(
                          'last-modified', auto_now=True, db_index=True)

    class Meta:
        '''Meta class for Base class'''
        abstract = True

class BookQuerySet(models.query.QuerySet):
    '''Modified Book QuerySet'''

    def get(self, *args, **kwargs):
        '''Modified get to support fetching either the id or an alias'''
        clone = super(BookQuerySet, self).filter(id=kwargs['pk']) | super(BookQuerySet, self).filter(aliases__value=kwargs['pk'])
        clone = clone.distinct()
        num = len(clone)
        if num == 1:
            return clone._result_cache[0]
        else:
            return super(BookQuerySet, self).get(*args, **kwargs)

class BookManager(models.Manager):
    '''Modified Book Manager to pass a modifed QuerySet'''

    def get_query_set(self):
        '''Deliver a modifed QuerySet'''
        return BookQuerySet(self.model)

class Book(BaseModel):
    '''
    Main storage for a Book object.
    '''

    id = models.CharField(max_length=30, primary_key=True,
                          help_text="The primary identifier of this title, \
                                     we get this value from publishers.")
    title = models.CharField(max_length=128,
                             help_text="The title of this book.",
                             db_index=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True, default=None,
                                   help_text="Very short description of \
                                              this book.")
    objects = BookManager()

    def __unicode__(self):
        return u"Book %s" % self.title

    class Meta:
        '''Meta class for Book class'''
        ordering = ['title']


class Alias(BaseModel):
    '''
    A book can have one or more aliases which

    For example, a book can be referred to with an ISBN-10
    (older, deprecated scheme), ISBN-13 (newer scheme),
    or any number of other aliases.
    '''

    book = models.ForeignKey(Book, related_name='aliases')
    value = models.CharField(max_length=255, db_index=True, unique=True,
                             help_text="The value of this identifier")
    scheme = models.CharField(max_length=40,
                             help_text="The scheme of identifier")

    def __unicode__(self):
        return '%s identifier for %s' % (self.scheme, self.book.title)

