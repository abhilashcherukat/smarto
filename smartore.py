__author__ = 'Abhilash'

import json
import web
import MySQLdb
import collections
import smtplib
import sys
import linecache

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urls = (
    '/', 'index',
    '/register','register',
    '/checkregistration','checkregistration',
    '/login','login',
)
# Server

#db = web.database(dbn='mysql', user='root', pw='igothelp2015', db='igothelp2015')

#Local

db = web.database(dbn='mysql', user='root', pw='', db='smartmeter')



class CommonFunctions():
    def NullFunction(self):
        status = {"Message": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)
    def LogError(self, message, APICall, LineNo):
        try:
            now = datetime.now()
            date = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "
            time = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
            entries = db.insert('errorLog', time=date+time,API=APICall,lineNumber=LineNo,details=str(message))
        except:
            pass
    def PrintException(self,API):
        try:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            print exc_obj
            line = linecache.getline(filename, lineno, f.f_globals)
            linepart=line.strip()
            #linePart="".join(linePart)
            msg=str(exc_obj)+"[" + linepart + "...]"
            return self.LogError(msg,API,lineno)#
        except:
            pass
    def SendMail(self, To, From, Subject, Html,Plain):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Subject
            msg['From'] = From
            msg['To'] = To
            part1 = MIMEText(Plain, 'plain',"utf-8")
            part2 = MIMEText(Html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            # Send the message via local SMTP server.
            #mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('abhilash.c@spurtreetech.com', 'Ab4i7@$h')
            mail.sendmail(From,To, msg.as_string())
            mail.quit()
            status = {"status": "Sucess", "message": "Mail Sent","statusCode":200,"MailSent":True}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)
        except smtplib.SMTPAuthenticationError:
            self.PrintException("Mail Sent Function")
            status = {"status": "Error", "message": "Authentication Error","statusCode":500,"MailSent":False}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)

        except Exception as e:
            self.PrintException("Mail Sent Function")
            status = {"status": "Error", "message": "Error Try Later","statusCode":str(e)}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)

class index:
    def GET(self):
        ComFnObj=CommonFunctions()
        try:
            k=0/0;
        except Exception as e:
            ComFnObj.PrintException("Index");
            return "This is an exception"
        else:
            return ComFnObj.NullFunction();

class checkregistration:
    def POST(self):
        user_data = web.input()

        try:
            email=user_data['email']
            entries = db.query("SELECT `id`, `fullname`,`email`,`startdt`,`enddt`,`authcode` FROM `tbl_user` WHERE `email`='"+str(email)+"'")
            rows = entries.list();
            if rows:
                JArray =collections.OrderedDict();

                JArray['Name']=rows[0]['fullname']
                JArray['Email']=rows[0]['email']
                JArray['Authcode']=rows[0]['authcode']
                JArray['StartDate']=str(rows[0]['startdt'])
                JArray['EndDate']=str(rows[0]['enddt'])

                status = {"Message": "Success", "Output":JArray,"statusCode":200}

            else:
                status = {"Message": "No such user", "Output": [],"statusCode":404}
        except Exception as e:
            status = {"Message": "Error", "Output": str(e.message),"statusCode":500}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)
    def GET(self):
        ComFnObj=CommonFunctions()
        return ComFnObj.NullFunction();

class login:
    def POST(self):
        user_data = web.input()

        try:
            Authcode=user_data['xblusen']
            Email=user_data['email']
            Password=user_data['passer']
            entries = db.query("SELECT `id`, `fullname`,email,authcode FROM `tbl_user` WHERE `authcode`='"+str(Authcode)+"' \
            and email='"+str(Email)+"' and password='"+str(Password)+"'")
            rows = entries.list();
            if rows:
                JArray =collections.OrderedDict()
                JArray['Name']=rows[0]['fullname']
                JArray['Email']=rows[0]['email']


                status = {"Message": "Success", "Output":JArray,"statusCode":200}

            else:
                status = {"Message": "Login Failed", "Output": [],"statusCode":404}
        except Exception as e:
            status = {"Message": "Error", "Output": str(e.message),"statusCode":500}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)

    def GET(self):
        ComFnObj=CommonFunctions()
        ComFnObj.NullFunction();

class modal_register:
    def POST(self):
        return 1
    def GET(self):
        ComFnObj=CommonFunctions()
        return ComFnObj.NullFunction();





if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
else:
    application = web.application(urls, globals()).wsgifunc()
