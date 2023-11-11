import logging
import os
import random
import requests
from typing import Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        # logging.StreamHandler(),
        logging.FileHandler('scrapper.log')
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_USER_AGENTS = [
    {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 12; moto g stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36v'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
]

DEFAULT_PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

class Scraper:
    def __init__(self) -> None:
        self.header_list = DEFAULT_USER_AGENTS

        self.session = requests.Session()
        self.session.proxies = DEFAULT_PROXIES

        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_session(self) -> requests.Session:
        return self.session
    
    def get_file(self, url) -> str:
        file = url.replace(":", "")
        file = file.replace("//", "/")
        file = file.replace("/", "_")
        file = file.replace(".", "_")
        return os.path.join(self.data_dir, file)
    
    def get_url(self, url, force_new=False) -> Optional[str]:
        file = self.get_file(url)
        if os.path.exists(file) and not force_new:
            return file

        try:
            logger.info(f"Accessing: {url}")

            req = self.get_session().get(url, headers=random.choice(self.header_list))
            req.close()

            with open(file, "w", encoding='utf-8') as fp:
                fp.write(req.text)

            return file
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error for {url}: {e}")
        except Exception as e:
            logger.error(f"An error occured for {url}: {e}")
        
        return None
