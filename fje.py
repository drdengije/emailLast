from __future__ import absolute_import, unicode_literals
#from celery import shared_task
import imaplib
import email as e_mail
#from .models import SendingDomains, SpamDomains, UsageLog, Addresses
import os
import selenium
from selenium.webdriver.common.by import By #import
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import csv
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import random
import time


cwdir = os.path.dirname(os.path.abspath(__file__))
webdriver_location = os.path.join(cwdir, r'\driver\geckodriver.exe')
print(webdriver_location)

class mail_obj():
   def __init__(self, mail, password, secret):
        self.mail = mail
        self.password = password
        self.secret = secret

def scan(i): #done
    email = i.Email
    password = i.Password
    print('maulchecker started')
    email_type = email.split('@')[-1]

    if email_type == 'gmail.com':
        imapa = 'imap.gmail.com'
        spam = '[Gmail]/Spam'
        inbox = 'INBOX'
    else:
        imapa = 'imap.yahoo.com'
        spam = 'Spam'
        inbox = 'INBOX'

    comn = imaplib.IMAP4_SSL(imapa, 993)
    comn.login(email, password)
    comn.select(spam)

    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    sending_list = SendingDomains.objects.all()
    spam_list = SpamDomains.objects.all()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        for i in sending_list:
            if i.Domain in raw['From']:
                inbox_count += 1
        spamm_count = 0
        for i in spam_list:
            if i.Domain in raw['From']:
                spamm_count += 1

    comn.select(inbox)
    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        inbox_count = 0
        for i in sending_list:
            if i.Domain in raw['From']:
                inbox_count += 1

        for i in spam_list:
            if i.Domain in raw['From']:
                spamm_count  += 1 #done

    us_log = UsageLog(
        EmailAddresses_ID=  Addresses.objects.get(pk=i.pk),
        Number_Opened = 0,
        Number_Clicked = index_count ,
        Number_Retreived_from_Spam = 0,
        Number_Spam = spamm_count,
    )
    us_log.save_base()




def login_gmail(i, driver):                #Pajce prepravio fju
    try:
        driver.get('http://www.gmail.com')
        #mail_url = 'https://mail.google.com/mail/u/0/#inbox'
        mail = i.Email
        password = i.Password
        sec_aw = i.Secret
        mail_url = 'https://mail.google.com/mail/u/0/#inbox'
        mail_input = driver.find_element_by_xpath("//input[@type='email']")
        mail_input.send_keys(mail)
        button = driver.find_element_by_xpath('//div[@class="VfPpkd-RLmnJb"]')
        button.click()
        time.sleep(10)
        mail_input = driver.find_element_by_xpath("//input[@type='password']")
        mail_input.send_keys(password)
        time.sleep(10)
        button = driver.find_element_by_xpath('//div[@id="passwordNext"]')
        button.click()
    except:
        driver.quit()
    if driver.current_url != mail_url:
        time.sleep(10)
        security_button = driver.find_element_by_xpath('//li[@class="JDAKTe cd29Sd zpCp3 SmR8"]')
        security_button.click()
        time.sleep(10)
        sec_answer_input = driver.find_element_by_xpath("//input[@id='secret-question-response']")
        sec_answer_input.send_keys(sec_aw)


            #button = driver.find_element_by_xpath("//div[@role='button']")
            #button.click()
            #time.sleep(10)
            #button2 = driver.find_element_by_xpath("//div[@role='button']")
            #button2.click()

        button = driver.find_element_by_xpath("//div[@class='FliLIb DL0QTb']")
        button.click()
        time.sleep(10)
        button2 = driver.find_element_by_xpath("//div[@class='U26fgb O0WRkf oG5Srb HQ8yf C0oVfc Zrq4w WIL89 k97fxb yu6jOd']")
        button2.click()




    time.sleep(10)
    driver.get(mail_url)
    time.sleep(5)



def remove_security(i, driver):           #Pajce prepravio fju
    securituy_link = 'https://myaccount.google.com/security'
    driver.get(securituy_link)
    time.sleep(10)
    less_secure = driver.find_element_by_xpath('//div[7]//article[1]//div[1]//div[1]//div[3]')
    less_secure.click()
    time.sleep(5)
    checkbox = driver.find_element_by_xpath("//div[@role='checkbox']")
    checkbox.click()
    time.sleep(5)
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    time.sleep(5)

def get_mailboxes(driver):
    more = driver.find_element(By.TAG_NAME, 'div')
    more.find_element(By.CLASS_NAME, 'n6')
    time.sleep(5)
    mb_arr = []
    for i in driver.find_elements_by_class_name('aim'):
        mb_arr.append(i.find_element_by_tag_name('a').get_attribute('href'))
    return mb_arr


def get_senders(driver):
    senderz = []
    for i in driver.find_elements(By.CLASS_NAME, 'bA4'):
        senderz.append(i.find_element(By.TAG_NAME, 'span').get_attribute('email'))
    return senderz

def spam_check(i, driver):     #Pajce "pravio" fju
    whitelist = 'dipik@raimarketingservices.com'
    spam_email_boxes = driver.find_elements_by_xpath("//div[@class='Cp']//tr")
    print(len(spam_email_boxes))
    for spam_email_box in spam_email_boxes:

        spam_email_class = spam_email_box.find_element_by_xpath(".//span[@email]")
        spam_email_text = spam_email_class.get_attribute('email')
        print('spam   ' + spam_email_text)
        with open('whitelist.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                print(str(row).strip("['']"))
                if (spam_email_text == str(row).strip("['']")):
                    transfer_write(spam_email_text, '   sent to mail')
                    elements = spam_email_box.find_elements_by_xpath(".//td[@data-tooltip='Select']")
                    for element in elements:
                        try:
                            print(element.get_attribute("innerHTML"))
                            element.click()
                            time.sleep(2)
                            #spam_button = driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]")
                            spam_button = driver.find_element_by_xpath("// div[contains(text(), 'Not spam')]")
                            spam_button.click()
                            time.sleep(2)
                        except:
                            print('spam_check: send from spam fail')




def email_check(i, driver):              #Pajce "pravio" fju
    email_boxes = driver.find_elements_by_xpath("//div[@class='Cp']//tr")
    print(len(email_boxes))

    for e,email_box in enumerate(email_boxes) :

        email_class = email_box.find_element_by_xpath(".//span[@email]")
        email_text = email_class.get_attribute('email')
        print('email   ' + email_text)
        with open('blacklist.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                print(str(row).strip("['']"))
                if (email_text == str(row).strip("['']")):
                    transfer_write(email_text, '   sent to spam')
                    #email_box.find_element_by_xpath(".//td[@data-tooltip='Select']").click()
                    elements = email_box.find_elements_by_xpath(".//td[@data-tooltip='Select']")
                    print(len(elements))
                    for element in elements:
                        try:
                            print(element.get_attribute("innerHTML"))
                            element.click()
                            time.sleep(2)
                            spam_button = driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div")
                            spam_button.click()
                            time.sleep(2)
                        except:
                            print('email_check: send to spam fail')




def read_email(i, driver):
    email_boxes = driver.find_elements_by_xpath("//div[@class='Cp']//tr")
    for e,email_box in enumerate(email_boxes) :
        time.sleep(2)
        try:
            email_class = email_box.find_element_by_xpath(".//span[@email]")
            email_text = email_class.get_attribute('email')
        except:
            break
        with open('whitelist.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if (str(row).strip("['']") == email_text):
                    #transfer_write(email_text, '   email opened')
                    for part in email_box.find_elements_by_xpath('.//td//div[@role="link"]'):
                        try:
                            part.click()
                            print(part.get_attribute('innerHTML'))
                            print('read_email function is working')
                            time.sleep(10)
                        except:
                            print('err')
                        reply_to_mail(i, driver)
                        try:
                            time.sleep(2)
                            transfer_write(email_text, 'email read links opened and answerd')
                            driver.back()
                            time.sleep(10)
                        except:
                            print('read_email function is NOT working')


def reply_to_mail(i, driver):
    try:
        linkovi = driver.find_elements_by_xpath('//div[@dir="ltr"]//a')
        for link in linkovi:
            time.sleep(2)
            link.click()
            time.sleep(5)
            allTabs = driver.window_handles
            driver.switch_to.window(allTabs[1])
            time.sleep(5)
            driver.close()
            time.sleep(5)
            driver.switch_to.window(allTabs[0])
            time.sleep(2)
    except:
        print("err")
    try:
        responses_list = ["thanks", "appreciate it", "hey great thank you!", "awesome"]

        time.sleep(3)
        reply_button = driver.find_element_by_xpath('(//tr//span[@role="link"])[1]')
        reply_button.click()
        time.sleep(2)
        message_box = driver.find_element_by_xpath('//div[@class="Am Al editable LW-avf tS-tW"]')
        message_box.send_keys(responses_list[random.randint(0,2)])
        time.sleep(5)
        send_button = driver.find_element_by_xpath('//div[@class="T-I J-J5-Ji aoO v7 T-I-atl L3"]')
        send_button.click()
        time.sleep(2)
    except:
        print('err')



def transfer_write(mail, description):

    with open('transfers.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([mail, description])




 







####### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tasks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ########


def mail_cheker(array):
    if len(array):
        for i in array:
            try:
                scan(i)
            except:
                print('nada')


def mail_cheker_selenium(array):
    no = 0
    nc =0
    ns = 0
    nr = 0
    if len(array):
        with  webdriver.Firefox(executable_path=webdriver_location) as driver:
            for i in array:
                try:
                    login_gmail(i, driver)
                    get_mailboxes(driver)
                    senders = get_senders(driver)
                except:
                    print('nada')
                us_log = UsageLog(
                    EmailAddresses_ID=Addresses.objects.get(pk=i.pk),
                    Number_Opened=no,
                    Number_Clicked=nc,
                    Number_Retreived_from_Spam=nr,
                    Number_Spam=ns,
                )
                us_log.save_base()


def single_security(i):
    try:
        with  webdriver.Firefox(executable_path=webdriver_location) as driver:
            login_gmail(i, driver)
            remove_securitu(i, driver)
    except:
        pass


def single_security_all(array):
    if len(array):
        with  webdriver.Firefox(executable_path=webdriver_location) as driver:
            for i in array:
                try:
                    login_gmail(i, driver)
                    remove_securitu(i, driver)
                except:
                    pass
