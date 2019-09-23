from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import msvcrt
import sys
import os
import time

# Whatsapp index their chat according in the order of 1,21,20,19...,2
# This is to check the first three messages in the index
whatsappIndexing = [1,21,20]
setTime = '1800 UTC+8'

# In seconds
refreshTime = 20

try:    
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://web.whatsapp.com/")
    input('Please enter the QR code, press any key to continue...')
except:
    print('[-] Access denied, please check your internet connection.')

# Main 
def main():
    os.system('cls')
    print('Welcome, this is a simple Whatsapp auto reply software! Please do not misuse it c:')
    while True:

        try:
            for i in whatsappIndexing:
                span = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div['+str(i)+']/div/div/div[2]/div[2]/div[2]/span[1]')

                # These magic numbers are from analysing the whatsapp xpath of the span tag that encapsulates the mute and status symbol
                if (span.size["width"] < 25 and span.size["height"] == 16 and span.size["width"] > 17) :
                    print('Message ' + str(i) + ' is being serviced')
                    send_msg(i)
                else :
                    print('Message ' + str(i) + ' is ignored')

            isPaused = readInput('Enter \'Pause\' to pause the program:', refreshTime)

            if(isPaused == "Pause"):
                goToPause()
                isPaused = ""

            # Need to reload to update the HTML body
            driver.get("https://web.whatsapp.com/")
        except:
            print('Something went wrong, retrying in ' + str(refreshTime) + ' seconds')

        time.sleep(refreshTime)

#To send
def send_msg(index):

    # Messages to be sent
    messages_to_send = ["[Assistant]: Hello, I am Ting's assistant.","He is currently sleeping/having a meeting/probably creating magic in his lab right now.","He will most probably reply you after " + setTime+ ". Thank you in advance for your patience."]

    user = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div['+str(index)+']')
    user.click()

    msg_box = driver.find_elements_by_class_name('_13mgZ')
    for i in messages_to_send:
        msg_box[0].send_keys(i)
        driver.find_element_by_class_name('_3M-N-').click()

    return

def goToPause():

    while True:
        options = input("Enter 'Return' to resume the program or 'Set Time' to set new time: ")

        if(options == "Return"):
            options = ""
            return
        elif(options == "Set Time"):
            setTime = options
            return
        else:
            continue
def readInput( caption, default, timeout = 5):

    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default))
    sys.stdout.flush()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 and (time.time() - start_time) > timeout:
            print("timing out, using default value.")
            break

    print('')  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

if __name__ == '__main__':
    main()
