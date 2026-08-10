import smtplib,mimetypes,os
from email.message import EmailMessage

sender = 'itachi13122003@gmail.com'
emailContainer = EmailMessage()
emailContainer['Subject'] = 'こんにちは'    
emailContainer['From'] = sender
emailContainer['To'] = 'prithika6384@gmail.com'
emailContainer.set_content('はじめまして、お元気ですか！')

files =[r'C:\Users\Agnie\Pictures\Sri Gallery\AiTeamImg.jpg']
for i in files:
    with open(i, 'rb') as file:
        data = file.read()
        fileName = file.name

    fileType = mimetypes.guess_type(fileName)[0]

    if fileType:
        maintype, subtype = fileType.split('/', 1)
    else:
        maintype, subtype = 'application', 'octet-stream'

    emailContainer.add_attachment(
        data,
        maintype=maintype,
        subtype=subtype,
        filename=os.path.basename(i)
    )

with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    with open(r'C:\Sri\Python Programs\EmailAutomation\AppPassword.txt','r') as passwordFile:password  = passwordFile.read()
    smtp.login(sender,password)
    smtp.send_message(emailContainer)
print("Email Sent Successfully !")
