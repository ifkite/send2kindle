from douban_api import Book
from sqlalchemy.sql import select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.sql import exists
from urllib2 import URLError
from book_db import Session
from book_db import Category,Publisher,Author,\
                    Book_info,Info_auth
#from book_except import MisArgExcept
import codecs
#PASSED
def check_title(name,book_dat):
    return name == book_dat.title

def insertion(sess,book_dat):
    pub_name = codecs.encode(book_dat.publisher,'utf-8')
    publisher = sess.query(Publisher).filter_by(pub_name=pub_name).first()
    if not publisher:
        publisher = Publisher(pub_name=pub_name)
        sess.add(publisher)
        sess.commit()
    title = codecs.encode(book_dat.title,'utf-8')
    isbn10 = codecs.encode(book_dat.isbn10,'utf-8')
    subtitle = codecs.encode(book_dat.subtitle,'utf-8')
    pub_id = publisher.pub_id
    book_info = sess.query(Book_info).filter_by(isbn10=isbn10).first()
    if not book_info:
        book_info = Book_info(title=title,\
                              isbn10=isbn10,\
                              subtitle=subtitle,\
                              pub_id=pub_id)
        sess.add(book_info)
        sess.commit()
    for auth in book_dat.author:
        auth_name = codecs.encode(auth,'utf-8')
        author = sess.query(Author).filter_by(auth_name=auth_name).first()
        if not author:
            author = Author(auth_name=auth_name)
            sess.add(author)
            sess.commit()
        book_id = book_info.book_id
        auth_id = author.auth_id
        info_auth = sess.query(Info_auth).\
                    filter(book_id==book_id,\
                           auth_id==auth_id).\
                    first()
        if not info_auth:
            info_auth = Info_auth(book_id=book_id,\
                                  auth_id=auth_id)
            sess.add(info_auth)
            sess.commit()

def store_info(name='',tag=''):
    #if name == '' and tag == '':
    #    raise MisArgExcept(**{'name':name,'tag':tag})
    book = Book()
    ins_state = False
    try:
        wrap = book.search(q=name,tag=tag)
        sess = Session()
        for b in wrap().books:
            wrap_dat = book.info(b.id)
            book_dat = wrap_dat()
            #preciss match
            if check_title(name,book_dat):
                insertion(sess,book_dat)
                ins_state = True
        sess.close()
    except URLError as e:
        print 'network maybe not connect'
        raise e
    return ins_state
