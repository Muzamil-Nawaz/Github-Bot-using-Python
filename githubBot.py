from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException

import time
import os
import sys




#  Initializing options for selenium web driver
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
# Give path to you chromedriver.exe here, to use selenium automation
# just put chromedriver.exe in same folder as your script 
driver = webdriver.Chrome(executable_path=os.path.join(sys.path[0],'chromedriver.exe'), options=option)


## also can add path like this 
# PATH = r'D:\\Code Programmin\\python\\Scraping\\Github-Bot\chromedriver.exe'
# driver = webdriver.Chrome(executable_path = PATH)

# Method used to login once at start of the automation
def login(user_name,pass_word):

    # Open github login page
    driver.get('https://github.com/login')
  

    # Let the browser load page completely by waiting 3 seconds
    time.sleep(2)

    # Input username
    username = driver.find_element_by_xpath('//*[@id="login_field"]')
    username.send_keys(user_name)
  

    # Input password
    password = driver.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(pass_word)



    # Click on sigin button
    sigin = driver.find_element_by_xpath('//*[@id="login"]/div[4]/form/div/input[12]')
    sigin.click()


    time.sleep(1)
    
    ## checking for invalid credentials alert box
    ## if it find alert box it means one of user provided credentials is wrong
    ErrorDict = {'error':None, 'message':None}

    try:
        error = driver.find_element_by_xpath('//*[@id="js-flash-container"]/div/div').text
        ErrorDict['error'] = True
        ErrorDict['message'] = error

    except NoSuchElementException:
        ErrorDict['error'] = False
        ErrorDict['message'] = None
        

    return ErrorDict    


    


# Method to take repository name to create, description to add, private flag, and readme flag 
# added extra parameter(uploading_folder_path) to avoid  manually adding folder path in line no: 116 
def github_repo( repository_name, uploading_folder_path,descriptions=False,
                private=False, readme=False):
      
    github_homepage_url = 'https://github.com/MyTest54/'

    # Create new repo.
    new_repo = driver.find_element_by_xpath('//*[@id="repos-container"]/h2/a')
    new_repo.click()
  
    # Enter Repo. name
    repositoryname = driver.find_element_by_xpath('//*[@id="repository_name"]')
    repositoryname.send_keys(repository_name)
  
    # Optional
  
    # Enter Description
    if descriptions:
        description = driver.find_element_by_xpath(
            '//*[@id="repository_description"]')
        description.send_keys(descriptions)
  
    # Private Mode
    if private:
        private = driver.find_element_by_xpath(
            '//*[@id="repository_visibility_private"]')
        private.click()
  
    # Create ReadMe File
    if readme:
        readme = driver.find_element_by_xpath(
            '//*[@id="repository_auto_init"]')
        readme.click()

    time.sleep(2)

    # Create new repo here using above details
    create = driver.find_element_by_xpath('//*[@id="new_repository"]/div[4]/button')
    create.click();

    # Now that our remote repo has been created, 
    # we need to upload content from our local machine folder to remote repo
    # Using OS module, we are executing git commands to initialize local repo, add content, 
    # do commit and finally push the content to remote repo


    print(os.chdir(uploading_folder_path+"\\"+repository_name))
    print(os.system('echo "# This repository is Uploaded with GITHUB Bot created by Muzamil Nawaz " >> README.md'))
    print(os.system('git init'))
    print(os.system('git add .'))
    print(os.system('git commit -m \"first commit\"'))
    print(os.system('git branch -M main'))

    # Here we are converting general repo name into repo specific format ('-' instead of spaces)

    print(os.system(f'git remote add origin https://github.com/Muzamil-Nawaz/'+generateRepoName(repository_name)+'.git'))
    print(os.system('git push -u origin main'))
    print(repository_name+" uploaded successfully.")

    # After creating a repo, and uploading content, move again to homepage for creating next one.
    driver.get("https://github.com/")
    # Wait for homepage to load completely
    time.sleep(3)


# Method used for converting general string to github_repo_format_string
def generateRepoName(str):
    # Replace all spaces in name with '-'
    return str.replace(" ","-")
    return str;


# Method to get all project directory names from the given path folder
def main(uploading_folder_path,github_username,github_password):
    
    os.chdir(uploading_folder_path)
    dirs = os.listdir()

    # Login with username password at start of automation
    # and checking error, if error is found the message will be printed    
    ErrorDict = login(github_username,github_password)
    if ErrorDict.get('error'):
        print(ErrorDict.get('message'))
        return
   

    # Loop through direcotories one by one by creating their remote repos    
    time.sleep(2)        
    for dir_name in dirs:
        github_repo(dir_name,uploading_folder_path)
        

if __name__ == '__main__':

    # Directory path where your projects are, which you want to upload on Github 
    uploading_folder_path = 'D:\\Code Programmin\\python\\Scraping\\tttt'
    github_username = 'awana4872@gmail.com'
    github_password = '@bleomessi'
    main(uploading_folder_path,github_username, github_password)