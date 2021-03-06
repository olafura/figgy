# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 5:01 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
'''Test for Tools'''

from django.test import TestCase
from lxml import etree
from storage.models import Book, Alias
import storage.tools


class TestTools(TestCase):
    '''Tests for the Tools module'''
    def setUp(self):
        pass

    def test_storage_tools_process_book_element_db(self):
        '''process_book_element should put the book in the database.'''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'A title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(Alias.objects.get(scheme='ISBN-10').value,
                         '0158757819')
        self.assertEqual(Alias.objects.get(scheme='ISBN-13').value,
                         '0000000000123')

    def test_storage_tools_aliased_id(self):
        '''process_book_element should work with an aliased id.'''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml_str_2 = '''
        <book id="0158757819">
             <title>Second title</title>
             <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
             </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        xml2 = etree.fromstring(xml_str_2)
        storage.tools.process_book_element(xml2)

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'Second title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(Alias.objects.get(scheme='ISBN-10').value,
                         '0158757819')
        self.assertEqual(Alias.objects.get(scheme='ISBN-13').value,
                         '0000000000123')

    def test_storage_tools_test_conflicting_alias(self):
        '''process_book_element should work with an alias that belongs
           to an other book.
        '''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml_str_2 = '''
        <book id="67890">
             <title>Second title</title>
             <aliases>
                <alias scheme="ISBN-10" value="2158757819"/>
                <alias scheme="ISBN-13" value="0000000000456"/>
             </aliases>
        </book>
        '''

        xml_str_3 = '''
        <book id="12345">
             <title>Third title</title>
             <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000456"/>
             </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        xml2 = etree.fromstring(xml_str_2)
        storage.tools.process_book_element(xml2)

        xml3 = etree.fromstring(xml_str_3)
        storage.tools.process_book_element(xml3)

        self.assertEqual(Book.objects.count(), 2)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'Third title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(book.aliases.filter(scheme='ISBN-10')[0].value,
                         '0158757819')
        self.assertEqual(book.aliases.filter(scheme='ISBN-13')[0].value,
                         '0000000000123')

    def test_storage_tools_test_conflicting_id(self):
        '''process_book_element should work with an id that belongs
           to an other book.
        '''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml_str_2 = '''
        <book id="67890">
             <title>Second title</title>
             <aliases>
                <alias scheme="ISBN-10" value="2158757819"/>
                <alias scheme="ISBN-13" value="0000000000456"/>
             </aliases>
        </book>
        '''
        xml_str_3 = '''
        <book id="0000000000456">
             <title>Third title</title>
             <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
             </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        xml2 = etree.fromstring(xml_str_2)
        storage.tools.process_book_element(xml2)

        xml3 = etree.fromstring(xml_str_3)
        storage.tools.process_book_element(xml3)

        self.assertEqual(Book.objects.count(), 2)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'Third title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(book.aliases.filter(scheme='ISBN-10')[0].value,
                         '0158757819')
        self.assertEqual(book.aliases.filter(scheme='ISBN-13')[0].value,
                         '0000000000123')

