#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
import os

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class EmailHandler(object):
    def __init__(self, smtpserver, user, pwd):
        self.smtp = smtplib.SMTP()
        self.smtpserver = smtpserver
        self.smtpuser = user
        self.smtppwd = pwd

    def generateAlternativeEmailMsgRoot(self, strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = strSubJect
        msgRoot['From'] = strFrom
        msgRoot['To'] = ",".join(listTo)
        if listCc:
            msgRoot['Cc'] = ",".join(listCc)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgContent = strMsgText.replace("\n","<br>") if strMsgText else ""
        msgContent += "<br>" + strMsgHtml if strMsgHtml else "" 

        # We reference the image in the IMG SRC attribute by the ID we give it below
        if listImagePath and len(listImagePath)>0:
            msgHtmlImg = msgContent + "<br>"
            for imgcount in range(0, len(listImagePath)):
                msgHtmlImg += '<img src="cid:image{count}"><br>'.format(count=imgcount)
            msgText = MIMEText(msgHtmlImg, 'html')
            msgAlternative.attach(msgText)
            # print(msgHtmlImg)

            # This example assumes the image is in the current directory
            for i,imgpath in enumerate(listImagePath):
                fp = open(imgpath, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image{count}>'.format(count=i))
                msgRoot.attach(msgImage)
        else:
            msgText = MIMEText(msgContent, 'html')
            msgAlternative.attach(msgText)

        return msgRoot

    # Send the email (this example assumes SMTP authentication is required)
    def sendemail(self, strFrom, listTo, strSubJect, strMsgText, strMsgHtml=None, listImagePath=None, listCc=None):
        msgRoot = self.generateAlternativeEmailMsgRoot(strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath)

        try:
            self.smtp = smtplib.SMTP()
            self.smtp.connect(self.smtpserver)
            self.smtp.login(self.smtpuser, self.smtppwd)
            if listCc:
                listTo = listTo + listCc
            self.smtp.sendmail(strFrom, listTo, msgRoot.as_string())
            self.smtp.quit()
        except Exception as e:
        	print "error"

if __name__ == "__main__" :
	smtpserver = 'smtp.163.com'
	username = 'aaa@bbb.com'
   	password = '123456'
	strFrom = 'aaa@bbb.com'
	strTo = ['aaa@bbb.com']
	strSubJect = 'dingtalk message'
	eh = EmailHandler(smtpserver,username,password)
	imgpath = "state.png"
	eh.sendemail(strFrom,strTo,"dingtalk message","dingtalk message","", [imgpath])
	
