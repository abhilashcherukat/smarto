__author__ = 'Abhilash'


__author__ = 'Abhilash'

import json
import web
import MySQLdb
import collections


urls = (
    '/', 'index',
    '/register','register',
    '/checkregistration','checkregistration',
    '/login','login',
)
# Server

#db = web.database(dbn='mysql', user='root', pw='igothelp2015', db='igothelp2015')

#Local

db = web.database(dbn='mysql', user='usr_smartmeter', pw='pPh4j7ZCHdTrX6SA', db='smartmeter')



class CommonFunctions():
    def NullFunction(self):
        status = {"Message": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)

class index:
    def GET(self):
        ComFnObj=CommonFunctions()
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
