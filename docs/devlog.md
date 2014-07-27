#develop log#

--------

* ISSUES  

  >*Jun.19th.2014*  
  >configuration about input directory

   >>solution  

    >> 1. * pkg_resources  

    >> 2. * relative path, with `from .module import class` and etc  

    >>   * `python -m`

  >*Jun.20th.2014*  
  >storage of account and passwd  

  >*Jun.21th.2014*
  >observer pattern may be a smart choice

  >*july.23th.2014*
  >change the way calling smtplib.SMTP.sendmail?
  >change the code about attachment, follow this:
  `
    import smtplib, os
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders

    def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
  `
  >*Jul.23th.2014*
  >send to many kindle accounts
  
* TO LEARN  