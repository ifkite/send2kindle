# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

class JsonDict(dict):
    def __getattr__(self,name):
        return self[name]

def douban_base(target):
    json_dict = JsonDict()
    response = urllib2.urlopen('https://api.douban.com/v2%s' % (target,))
    book_str = response.read()
    result = json.loads(book_str,object_hook=JsonDict)
    return result

class Book:
    def __init__(self):
        self._book = '/book'

    #PASSED
    def info(self,book_id=0):
        def wrapper():
            target = self._book+'/'+str(book_id)
            return douban_base(target)
        return wrapper

    #PASSED
    def get_tags(self,book_id=0):
        def wrapper():
            target = self._book+'/'+str(book_id)+'/tags'
            return douban_base(target)
        return wrapper

    #PASSED
    def by_isbn(self,isbn):
        def wrapper():
            target = self._book+'/isbn'+'/'+str(isbn)
            return douban_base(target)
        return wrapper

    #PASSED
    def search(self,q='',tag='',start=0,count=20):
        def wrapper():
            kargs = {'q':q,'tag':tag,'start':start,'count':count}
            para = urllib.urlencode(kargs)
            target = self._book+'/search?'+para
            return douban_base(target)
        return wrapper
