import feedparser
from datetime import datetime
import pytz
from feedgen.feed import FeedGenerator
import os
from bs4 import BeautifulSoup
import requests
import minify_html
import logging

logging.basicConfig(level=logging.INFO,
                    filename="file.log",
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

def remove_elements(soup, elements_to_remove):
    for element in elements_to_remove:
        for tag in soup.find_all(element):
            tag.decompose()
    logger.info("Removed elements: %s", ', '.join(elements_to_remove))

def get_clean_version(url):
    logger.info("Fetching page: %s", url)
    try:
        response = requests.get(url, headers=headers)
        html_content = response.text
        logger.info("Page fetched successfully")
        
        # Locate the relevant content
        start_comment = "<!-- start content-stage -->"
        end_comment = "<!-- start social bar -->"
        start_pos = html_content.find(start_comment)
        end_pos = html_content.find(end_comment)

        if start_pos == -1 or end_pos == -1:
            logger.warning("Could not find comments to extract content")
            return ""

        middle_part = html_content[start_pos + len(start_comment):end_pos].strip()
        soup = BeautifulSoup(middle_part, "html.parser")

        # Elements to remove
        elements_to_remove = ['svg', 'button', 'input', 'script']
        remove_elements(soup, elements_to_remove)

        # Remove div elements with class "related-content"
        for div in soup.find_all('div', class_='related-content'):
            div.decompose()
        logger.info("Removed 'related-content' div elements")

        minified_html = minify_html.minify(str(soup))
        logger.info("HTML content cleaned and minified successfully")
        return minified_html
    except Exception as e:
        logger.error("Error processing page %s: %s", url, e)
        return ""

# URLs to request RSS feeds from
rss_feed_urls = [
    'https://www.shz.de/lokales/schleswig/rss',
    'https://www.shz.de/lokales/gluecksburg-angeln/rss',
    'https://www.shz.de/lokales/flensburg/rss',
    'https://www.shz.de/deutschland-welt/schleswig-holstein/rss'
]

def get_unique_entries(feeds):
    unique_entries = {}
    for feed_url in feeds:
        logger.info("Fetching RSS feed: %s", feed_url)
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            entry_id = entry.get('id')
            if entry_id not in unique_entries:
                unique_entries[entry_id] = entry
            else:
                logger.info("Duplicate entry with ID %s found, skipping entry", entry_id)
    logger.info("Unique entries retrieved")
    return list(unique_entries.values())

def merge_rss_feeds(feed_urls):
    logger.info("Starting RSS feeds merge")
    unique_entries = get_unique_entries(feed_urls)
    sorted_entries = sorted(unique_entries, key=lambda entry: entry.published_parsed, reverse=True)
    logger.info("RSS feeds merged and sorted successfully")
    return sorted_entries

# Retrieve merged entries
merged_entries = merge_rss_feeds(rss_feed_urls)

# Set up the RSS feed generator
fg = FeedGenerator()
fg.id('www.shz.de')
fg.title('Lokale Nachrichten')
fg.link(href='https://shz.de', rel='alternate')
fg.description('Lokale Nachrichten aus dem Norden')
logger.info("FeedGenerator object for RSS feed created")

# Add new entries
for entry in merged_entries:
    try:
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.content(content=get_clean_version(entry.link), type="html")
        published_date = datetime(*entry.published_parsed[:6], tzinfo=pytz.timezone('Europe/Berlin'))
        fe.pubDate(published_date)
        logger.info("Entry with ID %s added", entry.id)
    except Exception as e:
        logger.error("Error adding entry with ID %s: %s", entry.id, e)

# Save the RSS feed to a file
feed_file = os.path.join(os.getcwd(), 'merged_feed.xml')
try:
    fg.atom_file(feed_file, pretty=True)
    logger.info("RSS feed file saved successfully at: %s", feed_file)
except Exception as e:
    logger.error("Error saving RSS feed file: %s", e)
