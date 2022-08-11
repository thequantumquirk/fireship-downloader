# NOTE: THIS IS ONLY FOR DEMONSTRATION PURPOSES. NO HARM IS INTENDED
# This is a fireship complete site ripper made by https://github.com/ShivamKumar2002 and https://telegram.dog/fosslover
# It can be used to download all courses and lessons from https://fireship.io
# You can check out our github account at https://github.com/ShivamKumar2002, https://github.com/fosslover69
# This script relies on yt-dlp to download videos
# Support: https://telegram.dog/fossaf

from bs4 import BeautifulSoup

import requests

from fireship_downloader import download_course


def main():
    # Index link for courses
    courses_page = 'https://fireship.io/courses/'

    # Index link for lessons
    lessons_page = 'https://fireship.io/lessons/'

    print("Getting Links For All Courses...")

    # Create soup of courses page
    courses_soup = BeautifulSoup(requests.get(courses_page).content, 'html.parser')

    # List of all courses elements
    all_courses = courses_soup.find_all('a', class_='card-course')

    # Get links for all courses
    courses_links = [f"https://fireship.io{a['href']}" for a in all_courses]

    print("\n\n\nGetting Links For All Lessons...")

    # Create soup of lessons page
    lessons_soup = BeautifulSoup(requests.get(lessons_page).content, 'html.parser')

    # List of all lessons elements
    all_lessons = lessons_soup.find_all('a', class_='card-lesson')

    # Get links for all lessons
    lessons_links = [f"https://fireship.io{a['href']}" for a in all_lessons]

    # Download all courses
    print("\n\n\nDownloading All Courses...")

    for course_link in courses_links:
        download_course(course_link)

    print("\n\n\nDownloaded All Courses")

    # Download all lessons
    print("\n\n\nDownloading All Lessons...")

    for lesson_link in lessons_links:
        download_course(lesson_link)

    print("\n\n\nDownloaded All Lessons")


if __name__ == "__main__":
    main()
