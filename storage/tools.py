# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
'''A tool module for Books to proccess the book elements'''

from storage.models import Book
from django.db.utils import IntegrityError


def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """

    book, created = Book.objects.get_or_create(pk=book_element.get('id'))
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')
    aliases = {}
    same_aliases = False
    book_aliases = {}
    for alias in book.aliases.values():
        book_aliases[alias['value']] = True

    for alias in book_element.xpath('aliases/alias'):
        scheme = alias.get('scheme')
        value = alias.get('value')
        aliases[scheme] = value
        if value in book_aliases:
            same_aliases = True

    if same_aliases == False and len(book_aliases) > 0:
        book, created = Book.objects.get_or_create(pk=aliases.values()[0])
        book.title = book_element.findtext('title')
        book.description = book_element.findtext('description')

    for scheme, value in aliases.items():
        try:
            book.aliases.get_or_create(scheme=scheme, value=value)
        except IntegrityError as e:
            pass

    book.save()

