# NOTE: THIS IS ONLY FOR DEMONSTRATION PURPOSES. NO HARM IS INTENDED
# This is a fireship course downloader made by https://telegram.dog/fosslover and https://github.com/ShivamKumar2002
# It can be used to download courses and lessons from https://fireship.io
# You can check out our github account at https://github.com/fosslover69, https://github.com/ShivamKumar2002
# This script relies on yt-dlp to download videos
# Support: https://telegram.dog/fossaf
import os

from bs4 import BeautifulSoup

from pathvalidate import sanitize_filepath

import requests

from yt_dlp import YoutubeDL

print("""
\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\t\tFireship Course Downloader
\t\t\t\t\t- @fosslover
\t\t\t\t\t- @ShivamKumar2002
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")


def get_course_links():
    while True:
        course_links = input("Enter the Fireship Course/Lesson Link (Multiple links are Supported Eg. link1 link2 ): ").split(" ")
        for course_link in course_links:
            course_link = course_link.strip()
            # Checking if the given links are from fireship.io
            if "fireship.io" not in course_link:
                print("\nEnter a Valid Fireship.io link")
                break
        else:
            break

    return course_links


def download_video(link, filename):
    # Custom configurations for yt-dlp
    ydl_opts = {
            # Output to the given filenames
            'outtmpl': {'default': filename + '.%(ext)s'},
            # Write subtitles
            'writesubtitles': 'true',
            # Download all subtitles
            'subtitleslangs': ['all'],
            # Add metadata and thumbnail to file
            'postprocessors': [
                    {'key': 'FFmpegMetadata', 'add_metadata': True},
                    {'key': 'EmbedThumbnail', 'already_have_thumbnail': False}
            ],
            # Download and merge the best video-only format and the best audio-only format,
            # or download the best combined format if video-only format is not availables
            'format': 'bv+ba/b',
            'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def download_course(course_link):
    session = requests.Session()

    # Get url content
    fireship_response = session.get(course_link).content

    # Use beautifulsoup for parsing html
    soup = BeautifulSoup(fireship_response, 'html.parser')

    videos_links = {}

    print(f"\nGetting Download Links :-")

    # If link is a course
    if "lessons" not in course_link:
        # Get course title and sanitize it for using as file or directory
        course_title = sanitize_filepath(soup.find("h1", attrs={"itemprop": "name"}).get_text().strip())
        print(f"\nCourse Title - {course_title}")

        # Initial Section
        current_section = "99. Unknown Section"
        section_counter = 1

        # Iterate over every child element of chapters
        for child in soup.find("div", class_="chapters-wrap").findChildren(recursive=False):
            # Arrange videos by sections
            if child.name == "h3":
                # Sanitize section name
                current_section = sanitize_filepath(f"{section_counter}. {child.get_text().strip()}")
                section_counter += 1

                print(f"Processing Section - {current_section}")

                # Add section for video links
                videos_links[current_section] = list()

                # Current child is no longer needed
                continue

            # Add link to appropriate sections
            elif child.name == "a":
                # Get video name
                file_name = sanitize_filepath(f'{child.find("strong").get_text().strip()} - {child.find("span", attrs={"class": "subtext"}).get_text().strip()}')
                print(file_name)

                # Fireship url of video
                video_fireship_link = f"https://fireship.io{child['href']}"

                # Add video info to video links
                videos_links[current_section].append({"file_name": file_name, "fireship_link": video_fireship_link})

            else:
                # If got unexpected child tag
                print("Unknown child element while getting links")
                print(child.prettify())
                print("Continuing from next elements...")
                continue

        # Download this course
        print(f"\n\n\nStarting Download for Course - {course_title}")

        # Get current directory
        script_dir = os.getcwd()

        # Make course directory
        course_dir = os.path.join(script_dir, course_title)
        os.makedirs(course_dir, exist_ok=True)

        # Iterate over every section
        for section_name, videos in videos_links.items():
            print(f"\nDownloading section - {section_name}")

            # Make sections directory
            section_dir = os.path.join(course_dir, section_name)
            os.makedirs(section_dir, exist_ok=True)

            # Download every video
            for video in videos:
                print(f'Downloading Video - {video["file_name"]}')
                download_video(video["fireship_link"], os.path.join(section_dir, video["file_name"]))

            # Go to course directory for downloading next section
            os.chdir(course_dir)

        print(f"\n\n\nDownloaded Course - {course_title}")
        os.chdir(script_dir)

    # If the link is a single lesson
    else:
        # Get lesson name
        lesson_title = sanitize_filepath(soup.find("h1", attrs={"itemprop": "name headline"}).get_text().strip())

        # Add lesson info to lesson links
        video = {"file_name": lesson_title, "fireship_link": course_link}

        # Download Lesson
        print(f'Downloading lesson - {video["file_name"]}')
        download_video(video["fireship_link"], video["file_name"])
        print(f"\n\n\nDownloaded Lesson - {lesson_title}")

    # Close requests session
    session.close()


def main():
    course_links = get_course_links()

    # Looping through the provided links
    for course_link in course_links:
        print(f"\n\n\nProcessing Link - {course_link}")

        download_course(course_link)


if __name__ == "__main__":
    main()
