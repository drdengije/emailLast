from selenium import webdriver
from fje import login_gmail
from fje import remove_security
import fje
import time
import csv


def klik(driver, xpath, s):
    try:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(s)
    except Exception as e:
        print(e)
def get_element(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath)
    except Exception as e:
        print('elementgetter-', xpath, e)

class mail_obj():
    def __init__(self, Email, Password, Secret):
       self.Email = Email
       self.Password = Password
       self.Secret = Secret
def granica(driver, xpath):
    try:
        granicaVar = get_element(driver ,xpath)
        return  int(granicaVar.text())
    except Exception as e:
        print('elementgetter-', xpath, e)
        return 0

#webdriver_location = 'C:\driver\geckodriver.exe'
webdriver_location = 'C:\gekodriver\geckodriver.exe'


with open ('emails.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            #print(row)
            i = mail_obj(row[0], row[1], row[2])

            with  webdriver.Firefox(executable_path=webdriver_location) as driver:
                try:
                    login_gmail(i, driver)
                except Exception as e:
                    print(e)

                #remove_security(i, driver)
                driver.maximize_window()
                time.sleep(5)
                klik(driver, "//div[@class='n6']", 5) #more

                klik(driver, "//div[@class='TN bzz aHS-aHO']", 10) #all mail


                time.sleep(5)
                #donja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[5]")
                #gornja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[6]")



                checking=0

                fje.email_check(i, driver)
                #driver.find_element_by_xpath('(//span[@class="Di"]//div[@class="T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3"])[3]').click()  # clicks the next page
                while(checking == 0):


                    klikenzi = driver.find_elements_by_xpath('//span[@class="Di"]//div[@class="T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3"]')
                    if (len(klikenzi) < 1):
                        checking=1
                    if (len(klikenzi) == 1):
                        for klikic in klikenzi:
                            try:
                                klikic.click()
                                print('------------------------------------------------------------------------------')
                                print("radi")
                            except:
                                checking = 1
                                print('------------------------------------------------------------------------------')
                                print("ne radi")   
                    print('------------------------------------------------------------------------------')    
                    print(len(klikenzi))
                    if (checking == 1):
                        break
                    for klikic in klikenzi:
                        try:
                            klikic.click()
                        except:
                            print("nije")
                        print(klikic)
                        time.sleep(2)

                    fje.email_check(i, driver)
                    #donja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[5]")
                    #gornja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[6]")

                time.sleep(10)

                klik(driver , "//div[@class='TN bzz aHS-bnv']", 5)# spam button click
                time.sleep(10)



                #donja_granica= granica(driver, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div/span/div[1]/span/span[1]/span[2]')
                #gornja_granica = granica(driver, '/html[1]/body[1]/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/span[1]/div[1]/span[1]/span[2]')
                izlaz = 0
                checking = 0
                fje.spam_check(i, driver)
                while (checking == 0):

                    time.sleep(2)
                    sledece_dugme = driver.find_elements_by_xpath('//span[@class="Di"]//div[@class="T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3"]') # clicks the next page
                    time.sleep(10)
                    print(len(sledece_dugme))
                    for dugme in sledece_dugme:
                        try:
                            dugme.click()
                            print('spam_check: next page button is working')
                        except:
                            print('spam_check: next page button is NOT working')
                            izlaz = 1
                    if (len(sledece_dugme) < 1):
                        checking = 1
                    if(izlaz == 1 ):
                        break   
                    fje.spam_check(i, driver)
                        #donja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[5]")
                        #gornja_granica = granica(driver, "(//span[@class='Dj']//span[@class='ts'])[6]")

                klik(driver, "//div[@class='TN bzz aHS-bnt']//div[@class='aio UKr6le']", 10) #inbox click
                checking = 0
                fje.read_email(i, driver)
                #qwe = driver.find_elements_by_xpath('//span[@class="Di"]//div[@class="T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3"]')
                while (checking == 0):

                    klikenzi = driver.find_elements_by_xpath('//span[@class="Di"]//div[@class="T-I J-J5-Ji amD T-I-awG T-I-ax7 T-I-Js-Gs L3"]')
                    if (len(klikenzi) < 1):
                        checking = 1
                    if (len(klikenzi) == 1):
                        for klikic in klikenzi:
                            try:
                                klikic.click()
                                print('------------------------------------------------------------------------------')
                                print("read_email function: one button found is working")
                            except:
                                checking = 1
                                print('------------------------------------------------------------------------------')
                                print("read_email function:  next page button is not clickable--found one")
                    print('------------------------------------------------------------------------------')
                    print(len(klikenzi))
                    if (checking == 1):
                        break
                    for klikic in klikenzi:
                        try:
                            klikic.click()
                        except:
                            print("read_email function:  next page button is not clickable--found more than one")
                        print(klikic)
                        time.sleep(2)

                    fje.read_email(i, driver)
                    time.sleep(10)





