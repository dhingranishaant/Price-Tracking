"""
Basic script.

Usage:
    amazonScript.py [--sendto=SENDTO] [--sendmail]
    amazonScript.py (-h | --help)

Options:
    -h --help  Help screen
    --sendmail  If you want to send mail, use this option
    --sendto=SENDTO  Recipient of the mail
"""
import requests  
from bs4 import BeautifulSoup #to get individual items requested
import smtplib #simple mail protocol to send and receive mails
import time #to run this script longer than usual
from docopt import docopt

URL = 'https://www.amazon.in/Havells-HD3162-Dryer-Concentrator-1565/dp/B08519FDLH/ref=sr_1_4_sspa?dchild=1&keywords=hair+dryer&qid=1611495939&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzTUg2MUNES0VUUjQmZW5jcnlwdGVkSWQ9QTAwMTQxNTAxQzZTV0hERUhCQzhZJmVuY3J5cHRlZEFkSWQ9QTAyNTIwMDgxNzgyQVpET1k0UkJPJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
#URL = 'https://www.google.com/search?q=vans&shoes'

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

def what_is_the_price(sendmail: bool, send_to: str = ""):
    page = requests.get(URL, headers = headers) #returns data from the website

    soup = BeautifulSoup(page.content, 'html.parser')
    #print(f"Soup = {soup}")
    # title = soup.find(id='productTitle').get_text()

    price = soup.find(id='priceblock_ourprice').get_text()  #getting the price but as a string 
    print(f"found price = {price}")
    converted_price = (price[1:7])
    PurchaseAmount = float(converted_price.strip().replace(",",""))

    if(PurchaseAmount > 1000.0 and sendmail):
        send_mail(send_to)
    else:
        print("Not sending any mail!")

    print(PurchaseAmount)
    #print(title.strip())


def send_mail(send_to: str):
    #using gmail
    #587 - port for connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Extended HELO (EHLO) is an Extended Simple Mail Transfer Protocol (ESMTP) command sent 
    # by an email server to identify itself when connecting to another email server to start the 
    # process of sending an email. It is followed with the sending email server's domain name. 
    # The EHLO command tells the receiving server it supports extensions compatible with ESMTP.
    server.ehlo()
    server.starttls() #encrypting connection
    server.ehlo()
    server.login('nishaantdhingra@gmail.com', 'tntwsuvfueiabmbj') 

    subject = "Price reduced!!!"
    body = "Check the amazon link https://www.amazon.in/Havells-HD3162-Dryer-Concentrator-1565/dp/B08519FDLH" \
"/ref=sr_1_4_sspa?dchild=1&keywords=hair+dryer&qid=1611495939&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlma" \
"WVyPUEzTUg2MUNES0VUUjQmZW5jcnlwdGVkSWQ9QTAwMTQxNTAxQzZTV0hERUhCQzhZJmVuY3J5cHRlZEFkSWQ9QTAyNTIwMDgxNzgyQVpET1k"\
"0UkJPJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
    msg = f"subject: {subject} \n\n {body}"
    
    server.sendmail(
        'nishaantdhingra@gmail.com',
        send_to,
        msg
    )

    print("EMAIL HAS BEEN SENT !")

    server.quit()

if __name__ == "__main__":
    args = docopt(__doc__)
    sendmail = args["--sendmail"] or False
    send_to = ""
    if sendmail:
        send_to = args["--sendto"] or "dhingranishaant@gmail.com"
        print(f"Sending to : {send_to}")
    what_is_the_price(sendmail, send_to)