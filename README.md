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
    * libyaml-dev
* nose
