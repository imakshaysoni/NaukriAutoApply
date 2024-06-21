import time
import schedule
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup


retry_time = 10

firstname='Akshay'                        #Add your LastName
lastname='Soni'                         #Add your FirstName
year_of_exp = 5
joblink=[]                          #Initialized list to store links: "https://www.naukri.com/mnjuser/recommendedjobs"
maxcount=20                        #Max daily apply quota for Naukri
maxtried = 100
keywords = [
    "Python Developer",
    "Python Software Engineer",
    "Python Programmer",
    "Python Backend Developer",
    "Python Full Stack Developer",
    "Python Web Developer",
    "Python Data Engineer",
    "Python Automation Engineer",
    "Python Application Developer",
    "Python/Django Developer",
    "Python Consultant",
    "Python Solutions Architect",
    "Python Team Lead",
    "Senior Python Developer",
    "Lead Python Developer",
    "Principal Python Developer",
    "Python Development Manager",
    "Python Technical Lead",
    "Python DevOps Engineer",
    "Python Software Development Engineer"
]
 # Add you list of role you want to apply
location = 'Pune'                       #Add your location/city name for within India or remote
applied =0                          #Count of jobs applied sucessfully
failed = 0                          #Count of Jobs failed
tried = 0
applied_list={
    'passed':[],
    'failed':[],
    'saved': []
}                                   #Saved list of applied and failed job links for manual review

import os, sys
import logging

def catch(error):
    """Method to catch errors and log error details"""
    _, _, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    msg = "%s : %s at Line %s." % (type(error), error, lineNo)
    logging.error(msg)
    print(f"Exception Raised: Error: {error}.")
    return False


def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    """Wait till element present. Default 30 seconds"""
    result = False
    driver.implicitly_wait(0)
    locator = locator.upper()

    for _ in range(timeout):
        time.sleep(0.99)
        try:
            if is_element_present(driver, getObj(locator), elementTag):
                result = True
                break
        except Exception as e:
            print("Exception when WaitTillElementPresent : %s" % e)
            pass

    if not result:
        print("Element not found with %s : %s" % (locator, elementTag))
    driver.implicitly_wait(3)
    return result


def is_element_present(driver, how, what):
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def getObj(locatorType):
    """This map defines how elements are identified"""
    map = {
        "ID": By.ID,
        "NAME": By.NAME,
        "XPATH": By.XPATH,
        "TAG": By.TAG_NAME,
        "CLASS": By.CLASS_NAME,
        "CSS": By.CSS_SELECTOR,
        "LINKTEXT": By.LINK_TEXT,
    }
    return map[locatorType.upper()]


def GetElement(driver, elementTag, locator="ID"):
    """Wait max 15 secs for element and then select when it is available"""
    try:

        def _get_element(_tag, _locator):
            _by = getObj(_locator)
            if is_element_present(driver, _by, _tag):
                return WebDriverWait(driver, 15).until(
                    lambda d: driver.find_element(_by, _tag)
                )

        element = _get_element(elementTag, locator.upper())
        if element:
            return element
        else:
            print("Element not found with %s : %s" % (locator, elementTag))
            return None
    except Exception as e:
        return f"Failed: {e}"

def main():
    applied = 0
    tried = 0
    failed = 0
    saved = 0
    
    try:
    
        try:
            # profile_directory = '/Users/akshay.soni/Library/Application Support/Firefox/Profiles/jxd5yh7s.NaukriAutoApply'
            # profile = webdriver.FirefoxProfile(profile_directory)
            # driver = webdriver.Firefox(profile)
    
            # M2
            # profile_path = "/Users/akshay.soni/Library/Application Support/Firefox/Profiles/"
            # profile = webdriver.FirefoxProfile(profile_path) #Add your Root directory path
            # # print(profile_paths)
            # # profile = webdriver.FirefoxProfile("/Users/akshay.soni/Library/Application Support/Firefox/Profiles/jxd5yh7s.NaukriAutoApply") #Add your Root directory path
            # driver = webdriver.Firefox(profile)
    
            # M3
            profile_directory = '/Users/akshay.soni/Library/Application Support/Firefox/Profiles/jxd5yh7s.NaukriAutoApply'
            profile = webdriver.FirefoxProfile(profile_directory)
    
            options = webdriver.FirefoxOptions()
            options.profile = profile
    
            driver = webdriver.Firefox(options=options)
        except Exception as e:
            print(f'Webdriver exception: {e}')
            return False
    
        time.sleep(10)
        for k in keywords:
            for i in range(2):
                if location=='':
                    url = "https://www.naukri.com/"+k.lower().replace(' ','-')+"-"+str(i+1)
                else: url = "https://www.naukri.com/"+k.lower().replace(' ','-')+"-jobs-in-"+location.lower().replace(' ','-')+"-"+str(i+1)
                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source,'html5lib')
                results = soup.find(class_='styles_middle-section-container__iteRZ')
                job_elems = results.find_all(class_='srp-jobtuple-wrapper')
                for job_elem in job_elems:
                    joblink.append(job_elem.find('a',class_='title').get('href'))

    
        for job in joblink:
            time.sleep(3)
            driver.get(job)
            if applied <=maxcount and tried <= maxtried:
                try:
                    tried+=1
                    time.sleep(3)
                    # driver.find_element_by_xpath("//*[text()='Apply']").click()
                    # driver.find_element_by_xpath('//*[@id="apply-button"]').click()
                    already_applied_location = '//*[@id="already-applied"]'
                    apply_btn_location = '//*[@id="apply-button"]'
                    save_btn_location = '//*[@class="styles_save-job-button__WLm_s"]'
                    already_saved_location = '//*[@class="styles_saved-button__Cw_V_"]'
                    applyBtn = GetElement(driver, apply_btn_location, locator="XPATH")
                    saveBtn = GetElement(driver, save_btn_location, locator="XPATH")
                    alreadyAppliedBtn = GetElement(driver, already_applied_location, locator="XPATH")
                    alreadySavedButton = GetElement(driver, already_saved_location, locator="XPATH")
    
                    if applyBtn:
                        applyBtn.click()
                        time.sleep(5)
    
                        # Check for popup
                        print("Checking for popup and Question")
                        question_location = '//*[@class="botMsg msg"]'
                        print("Checking for Question")
                        if GetElement(driver, question_location, locator="XPATH"):
                                print("Question Found")
                                question_contains_location = '//span[contains(text(), "years of experience")]'
                                question = GetElement(driver, question_contains_location, "XPATH")
                                if question:
                                    print("Question Exist")
                                    question.send_keys(year_of_exp)
                                    savebtn_location = '//*[@class="sendMsg"]'
                                    save_ans_btn = GetElement(driver, savebtn_location, "XPATH")
                                    if save_ans_btn:
                                        print("Answer Save Button")
                                        save_ans_btn.click()
    
                        time.sleep(2)
                        success_check_location = '//*[@class="apply-status-header green"]'
                        if GetElement(driver, success_check_location, locator="XPATH"):
                            applied += 1
                            applied_list['passed'].append(job)
                            print('Applied for ', job, " Count", applied)
                        else:
                            print("Apply Failed.")
                            applied_list['failed'].append(job)
                            continue
    
                    elif saveBtn:
                        saveBtn.click()
                        applied_list['saved'].append(job)
    
                    elif alreadyAppliedBtn:
                        print("Already Applied:")
                        applied_list['passed'].append(job)
    
    
                    elif alreadySavedButton:
                        print("Already Saved.")
                        applied_list['saved'].append(job)
    
                    else:
                        print(f"Job is neither appled, saved, or Already Applied, Already Saved,"
                              f" Skip Job: {job}")
                        continue
    
                except Exception as e:
                    failed+=1
                    applied_list['failed'].append(job)
                    print(e, "Failed " ,failed)
    
                try:
                    if driver.find_element_by_xpath("//*[text()='Your daily quota has been expired.']"):
                        print('MAX Limit reached closing browser')
                        driver.close()
                        break
                    if driver.find_element_by_xpath("//*[text()=' 1. First Name']"):
                        driver.find_element_by_xpath("//input[@id='CUSTOM-FIRSTNAME']").send_keys(firstname)
                    if driver.find_element_by_xpath("//*[text()=' 2. Last Name']"):
                        driver.find_element_by_xpath("//input[@id='CUSTOM-LASTNAME']").send_keys(lastname);
                    if driver.find_element_by_xpath("//*[text()='Submit and Apply']"):
                        driver.find_element_by_xpath("//*[text()='Submit and Apply']").click()
                except:
                    pass
    
            else:
                driver.close()
                break
        print('Completed applying closing browser saving in applied jobs csv')
    
        try:
            driver.close()
        except:
            pass
    
        # Format the log content
        output_file = "naukri_auto_apply_response.txt"
    
        execute_finished = datetime.now()
        success = applied_list['passed']
        failed = applied_list['failed']
        saved = applied_list['saved']
    
        log_content = (
            f"\n\nExecute At: {execute_finished}\n\n"
            "Success:\n" + ''.join([f"- {url}\n" for url in success]) + "\n"
            "Failed:\n" + ''.join([f"- {url}\n" for url in failed]) + "\n"
            "Saved:\n" + ''.join([f"- {url}\n" for url in saved]) + "\n"
        )
    
        with open(output_file, 'w') as file:
            file.write(log_content)

        return True
    except Exception as err:
        print(f"job Failed: Error: {err}")
        return False
    
    finally:
        driver.close()
    

def job():
    try:
        print("Job execution started.")
        success = main()
        print(f"Job Response: {success}")
        if success:
            return True
        return False
    except Exception as e:
        return catch(e)


def retry_job():
    success = job()
    print(f"Retry Job Response: {success}")
    if success:
        print("Job execution finished, Clearing the retry_job")
        # If the retry job succeeds, clear the retry schedule
        schedule.clear('retry_job')
        print("Retry job cleared.")
    if not success:
        print(f"Retry job also failed, It will retry again in {retry_time} minutes")


def schedule_main_job():
    success = job()
    print(f"Scheduled Job Response: {success}")
    if success:
        print("Job execution finished, Resume Updated.")
    if not success:
        print(f"Job execution failed, Scheduling retry job for every {retry_time} minutes.")
        # Tag the retry job so it can be cleared later
        schedule.every(retry_time).minutes.do(retry_job).tag('retry_job')
        print("Retry job scheduled.")


# Initial scheduling of the main job
schedule.every().day.at("12:00").do(schedule_main_job)

while True:
    print(f"Checking job scheduler: Time: {datetime.now()}")
    schedule.run_pending()
    time.sleep(10)  # check & schedule job after every 20 minutes
