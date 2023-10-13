import os
import threading
from queue import Queue
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from tqdm import tqdm
import logging
from time import sleep

# create an HTML Session object
session = HTMLSession()

# base url
url = 'https://www.wcostream.org/anime/jujutsu-kaisen'

# get the html

r = session.get(url)

# create the soup object
html = r.html

# find all the episodes
episodes = html.find('#catlist-listview li a')

urls = [episode.attrs['href'] for episode in episodes]

def download_video(url_range):
    firefox_options = Options()
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--headless')
    service = Service('/snap/bin/firefox.geckodriver')

    driver = webdriver.Firefox(service=service, options=firefox_options)

    for detailurl in url_range:
        driver.get(detailurl)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        iframe = driver.find_element(By.ID, 'frameNewcizgifilmuploads0')
        if iframe is None:
            print('No iframe found in the HTML')
            continue
        iframe_url = iframe.get_attribute('src')

        # switch to the iframe window
        driver.switch_to.frame(iframe)
        sleep(3)
        video = driver.find_element(By.TAG_NAME, 'video')
        if video is None:
            print('No video found in the HTML')
            continue
        video_url = video.get_attribute('src')
        print(video_url)

        # https://www.wcostream.org/fire-force-season-2-episode-22-english-dubbed
        filename = detailurl.split('/')[-1] + '.mp4'
        if os.path.exists(filename):
            print(f'{filename} already exists, skipping...')
            continue
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Range': 'bytes=0-',
            'Referer': detailurl,
            'Origin': 'https://www.wcostream.org',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        try:
            r = session.get(video_url, headers=header, stream=True)
            r.raise_for_status()
        except Exception as e:
            print(f'Error downloading {filename}: {e}')
            continue

        total_size = int(r.headers['Content-Length']) 

        sleep(3)

        with open(filename, 'wb') as f:
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True) 
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                progress_bar.update(len(chunk))


def download_in_batches(urls, batch_size=3):
    url_queue = Queue()
    for url in urls:
        url_queue.put(url)

    while not url_queue.empty():
        threads = []
        for i in range(batch_size):
            if not url_queue.empty():
                url_range = []
                for j in range(batch_size):
                    if not url_queue.empty():
                        url_range.append(url_queue.get())
                thread = threading.Thread(target=download_video, args=(url_range,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            try:
                thread.join()
            except Exception as e:
                logging.error(f"Error occurred while downloading video: {e}")

download_in_batches(urls)