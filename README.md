# Send2kindle #
Send books to kindle automatically.  
Platform: Ubuntu-12.04-LST

## Usage ##
0. Make sure that [watchdog](https://github.com/gorakhargosh/watchdog) installed.  
1. Config `USER` `KINDLE_ACCOUNT` and `BOOK_PATH` in config.py.  
2. Executing `python sendmail.py` which will start listening the directory, a mail will be  
   sent when one file created in that directory.  
3. To stop, `CTRL-C`.  

## Requirements ##
* python2.7
* watchdog
>  libyaml-dev  

* sqlalchemy
>  mysql-python  
> >  mysql

* nose

## Configure ##
1. [Create] new user in mysql, or change code in `book_db.py`.  
   First, use root account to connet to mysql.
   Second, create user named `book_admin` with no password, as the following:  
   ```
   mysql>GRANT ALL PRIVILEDGES ON *.* TO 'book_admin'@'localhost WITH GRANT OPTION';
   ```
   
[Create]:(http://dev.mysql.com/doc/refman/5.1/zh/database-administration.html#adding-users)
