from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.webdriver.common.by import By

# create an HTML Session object
session = HTMLSession()

# base url
url = 'https://www.wcostream.org/anime/fire-force'

# get the html

r = session.get(url)

# create the soup object
html = r.html

# find all the episodes
episodes = html.find('#catlist-listview li a')

urls = []
for episode in episodes:
    url = episode.attrs['href']
    urls.append(url)
print(urls)

firefox_options = Options()
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--headless')
service = Service('/snap/bin/firefox.geckodriver')

driver = webdriver.Firefox(service=service, options=firefox_options)

for detailurl in urls:
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
    filename = detailurl.split('/')[-1]
    print(filename)

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

    r = session.get(video_url, headers=header, stream=True)
    print(r.headers)
    # save the video
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

