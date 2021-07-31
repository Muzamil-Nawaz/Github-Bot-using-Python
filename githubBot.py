
from selenium import webdriver 

import time
import os
import sys


# Directory path where your projects are, which you want to upload on Github as Seperate Repos
uploading_folder_path = "G:\\Netbeans Project\\Uploaded On Github"

#  Initializing options for selenium web driver
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])

# Give path to you chromedriver.exe here, to use selenium automation
driver = webdriver.Chrome(executable_path=os.path.join(sys.path[0],'chromedriver.exe'), options=option)

# Method used to login once at start of the automation
def login(user_name,pass_word):

    # Open github login page
    driver.get('https://github.com/login')
  
    # Username
    username = driver.find_element_by_xpath('//*[@id="login_field"]')
    # Input username
    username.send_keys(user_name)
  

    # Password
    password = driver.find_element_by_xpath('//*[@id="password"]')
    # Input password
    password.send_keys(pass_word)

    # Let the browser load page completely by waiting 3 seconds
    time.sleep(3)

    # Click on sigin button
    sigin = driver.find_element_by_xpath(
        '//*[@id="login"]/div[4]/form/div/input[12]')
    sigin.click()
  
    # Wait for home page to get loaded completely
    time.sleep(5)


# Method to take repository name to create, description to add, private flag, and readme flag 
def github_repo( repository_name, descriptions=False,
                private=False, readme=False):
      
    
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
    os.chdir(uploading_folder_path+"\\"+repository_name)
    print(os.system('echo "# This repository is Uploaded with GITHUB Bot created by Muzamil Nawaz " >> README.md'))
    print(os.system('git init'))
    print(os.system('git add .'))
    print(os.system('git commit -m \"first commit\"'))
    print(os.system('git branch -M main'))
    # Here we are converting general repo name into repo specific format ('-' instead of spaces)
    print(os.system('git remote add origin https://github.com/Muzamil-Nawaz/'+generateRepoName(repository_name)+'.git'))
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
def getDirs(path):
    os.chdir(path)
    dirs = os.listdir()
    # Login with username password at start of automation
    login("your-github-username-here", "your-github-password-here")
    # Loop through direcotories one by one by creating their remote repos
    for dir in dirs:
        github_repo(dir)
        

getDirs(uploading_folder_path)