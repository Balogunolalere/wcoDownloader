
Anime Video Downloader
======================

This program downloads anime videos from [www.wcostream.org](http://www.wcostream.org) using Selenium and multithreading.

Requirements
------------

*   Python 3
*   Requests-HTML
*   Selenium
*   tqdm
*   Firefox driver (geckodriver)

Usage
-----

1.  Update the `url` variable to the anime page URL you want to scrape (e.g. [https://www.wcostream.org/anime/jujutsu-kaisen](https://www.wcostream.org/anime/jujutsu-kaisen))
2.  Run the code:

Copy code

`python anime_downloader.py`

3.  The program will scrape the page to find all the episode links, then launch Firefox browsers to go through each episode page and extract the video URL.
4.  The video will be downloaded using Requests and saved with the episode filename. A progress bar is shown using tqdm.
5.  Videos are downloaded in batches using multithreading to speed up the process. The batch size can be configured by changing the `_batch_size_` parameter.

Code Overview
-------------

*   `session = HTMLSession()` - Creates a Requests-HTML session to send requests and parse HTML
*   `r = session.get(url)` - Gets the HTML of the main anime page
*   `html.find(...)` - Parses the HTML to find all the episode links
*   `download_video()` - The function that handles downloading one video given the episode URL
    *   Uses Selenium to launch Firefox and extract the video URL from the iframe
    *   Downloads the video with Requests
*   `download_in_batches()` - Manages the multithreaded batch downloading
    *   Puts episode URLs into a queue
    *   Starts threads to call `download_video` concurrently
*   Threading allows multiple videos to be downloaded simultaneously to improve speed
*   Videos are saved with the episode filename extracted from the URL
*   Includes error handling for missing elements and video download issues

Improvements
------------

*   Add option to specify download directory
*   Support logins/cookies to access restricted content
*   Retry failed downloads
*   Add MP4Box to properly stitch segmented video files
*   Migrate to Playwright instead of Selenium for more stable browser automation

Credits
-------

The web scraper is for educational purposes only.


