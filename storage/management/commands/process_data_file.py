# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:56 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
'''Module to parse XML files and add them to Books'''

from django.core.management.base import BaseCommand, CommandError

from lxml import etree
import storage.tools


class Command(BaseCommand):
    '''Parses the XML file you give it'''
    args = '<filename filename2 filename3 ...>'
    help = 'Process an xml file '

    def handle(self, *args, **options):
        for filename in args:
            with open(filename, 'rb') as fh:
                print "Importing %s into database." % filename
                book_node = etree.parse(fh).getroot()
                storage.tools.process_book_element(book_node)

