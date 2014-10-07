from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (MetaData, Table, ForeignKey, Column, Integer, String)
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://book_admin:@localhost/dou_book',\
                       encoding='utf-8')
metadata = MetaData()
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Category(Base):
    __tablename__ = 'category'
    catg_id = Column(Integer, primary_key=True,\
                     nullable=False,autoincrement=True)
    catg_name = Column(String(255),nullable=False,unique=True)

    def __repr__(self):
        return "<Category(catg_name=%s)>" % (self.catg_name)

class Publisher(Base):
    __tablename__ = 'publisher'
    pub_id = Column(Integer, primary_key=True,\
                    nullable=False,autoincrement=True)
    pub_name = Column(String(255),nullable=False,unique=True)

    def __repr__(self):
        return "Publisher<(pub_name=%s)>" % (self.pub_name)

#can not avoid the case that authors who have same name
class Author(Base):
    __tablename__ = 'author'
    auth_id = Column(Integer, primary_key=True,\
                     nullable=False,autoincrement=True)
    auth_name = Column(String(255),nullable=False,unique=True)

    def __repr__(self):
        return "Author<auth_name=%s>" % (self.auth_name)

class Book_info(Base):
    __tablename__ = 'book_info'
    book_id = Column(Integer, primary_key=True,\
                     nullable=False,autoincrement=True)
    title = Column(String(255), nullable=False)
    isbn10 = Column(String(24), nullable=True,unique=True)
    subtitle = Column(String(255), nullable=True)
    catg_id = Column(Integer, ForeignKey('category.catg_id'),\
                     nullable=True)
    pub_id = Column(Integer, ForeignKey('publisher.pub_id'),\
                    nullable=True)

    def __repr__(self):
        return "<Book_info(title=%s, isbn10=%s, subtitle=%s)>" %\
                   (self.title,self.isbn10,self.subtitle)

class Info_auth(Base):
    __tablename__ = 'info_auth'
    book_id = Column(Integer, ForeignKey('book_info.book_id'),\
                     primary_key=True, nullable=False)
    auth_id = Column(Integer, ForeignKey('author.auth_id'),\
                     primary_key=True, nullable=False)

#def get_or_create(sess,model,**kargs):
#    ins = sess.query().filter_by(**kargs).first()
#    if ins:
#        return ins,False
#    else:
#        ins = model(**kargs)
#        sess.add(model)
#        return ins,True

Base.metadata.create_all(engine)
