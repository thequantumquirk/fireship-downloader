# This is a fireship course downloader made by https://telegram.dog/fosslover
# which is used to download courses from https://fireship.io (You can download pro courses too XD)
# You can check out my github account at https://github.com/fosslover69
# This script relies on yt-dlp use `pip install yt-dlp` to install it
# Support: https://telegram.dog/fossaf

from re import *
import subprocess
import urllib.request
import os

print("""
\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\t\tFireship Course Downloader
\t\t\t\t\t- @fosslover
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

while(True):
    try:
        userMenuChoice=int(input("""
1. Download Course/Lesson Here
2. Download Course/Lesson in Seperate Folder
Enter Your Choice: """))
        if userMenuChoice != 1 and userMenuChoice != 2:
            raise ValueError
        break
    except (ValueError):
        print("Enter a Valid Choice")
    except (KeyboardInterrupt):
        print("\nExiting.....")
        exit()

while(True):
    try:
        courseLinkInput = input("""
Enter the Fireship Course/Lesson Link (Multiple links are Supported Eg. link1 link2 ): """)
        # Spliting the links if multiple links are given
        courseLinkList = courseLinkInput.split(" ")
        for courseLink in courseLinkList:
            courseLink = courseLink.strip()
            # Checking if the given links are from fireship.io
            if "fireship.io" not in courseLink:
                raise ValueError
            # Checking if the given links are valid
            fireshipResponse = urllib.request.urlopen(courseLink).read().decode("utf-8")
        break
    except (ValueError):
        print("\nEnter a Valid Fireship.io link")
    except (KeyboardInterrupt):
        print("\nExiting.....")
        exit()
# Looping through the provided links
for courseLink in courseLinkList:
    # Striping the link incase if there's duplicated whitespace
    courseLink = courseLink.strip()
    # Connecting to the url and fetching the HTML
    fireshipResponse = urllib.request.urlopen(courseLink).read().decode("utf-8")
    # Parsing and Formatting the obtained HTML response
    fireshipResponse = fireshipResponse.split("\n")
    stripedResponse=[]
    for element in fireshipResponse:
        element = element.strip()
        stripedResponse.append(element)
    
    linkList=[]
    # Parsing through the <header> tag to fetch the course title
    courseTitle = findall('<h1 .*>(.*?)</h1>', str(stripedResponse), DOTALL)
    print(courseTitle)
    courseTitle = sub("\[\"', '","",str(courseTitle))
    courseTitle = sub("', '\"\]", "", str(courseTitle))
    courseTitle = courseTitle
    # Fetching the course Link
    if "lessons" in courseLink:
            linkList.append(courseLink)
    # Fetching all the video links if its a course 
    else:
        url=[]
        for line in stripedResponse:
            line=line.strip()
            if line.startswith('<a href="/courses/'):
                line=findall(r'"(.*?)"', line)
                url.append(line)
        for line in url:
            for link in line:
                link="https://fireship.io/"+link
                linkList.append(link)
    
    # Storing the Links in a Textfile to make batch process with yt-dlp
    fireshipLinkOut=open(courseTitle+".txt", "w")
    
    for link in linkList:
        fireshipLinkOut.write(link+"\n")
    fireshipLinkOut.close()
    
    #read the links as list
    fireshipLinkIn=open(courseTitle+".txt", "r")
    linkList=fireshipLinkIn.readlines()
    fireshipLinkIn.close()


    # Downloading the Lessons with yt-dlp according to the users choice
    try:
        if userMenuChoice==1:
            for link in linkList:
                file_name=link.split("/")[-2]+".mp4" #takes /n as last of list, that's why -2 is used
                print("Downloading "+file_name)
                subprocess.run(["yt-dlp","-f","mp4",link,"-o"+file_name])
                print("Downloaded "+file_name)
            print("\nDownloaded All Lessons")

        if userMenuChoice==2:
            os.makedirs(courseTitle,exist_ok=True)
            #download the links
            for link in linkList:
                file_name=link.split("/")[-2]+".mp4" #takes /n as last of list, that's why -2 is used
                print("Downloading "+file_name)
                subprocess.run(["yt-dlp","-f","mp4",link,"-o"+file_name,"-P",courseTitle])
                print("Downloaded "+file_name)
            print("\nDownloaded All Lessons")
    except (FileNotFoundError):
        print("\nPlease install \"yt-dlp\" ")
        exit()


# Cleaning up text files created for batch operations
for fileName in os.listdir():
    if fileName.endswith(".txt"):
        os.remove(fileName)