#!/usr/bin/env python3

import json
import requests
from datetime import datetime
import time

BASE_URL = 'https://reddit.com/subreddits/new.json?nsfw=1&include_over_18=on&limit=100'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
TIMEOUT = 100
MAX_DESC_LEN = 500
MAX_RECORDS_PER_FILE = 10000000 # CSV row count per file
OUT_FILE_SUFFIX = '.out.csv'
TEXT_FILE = 'reddit_subreddits.txt'
MAX_RETRIES = 0  # Maximum number of retries for failed requests
PAUSE_INTERVAL = 60  # Pause interval for every n loops

def main():
    target = f'./{datetime.now().isoformat()}{OUT_FILE_SUFFIX}'
    with open(target, 'w', encoding='utf-8') as file:
        file.write('Subreddit,Subscribers,NSFW,Description,Status\n')
    with open(TEXT_FILE, 'r') as file:
        subreddits = [line.strip() for line in file]
    count = 1
    for i, subreddit in enumerate(subreddits, start=1):
        for attempt in range(MAX_RETRIES + 1):
            try:
                url = f'https://www.reddit.com/r/{subreddit}/about.json'
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    subscribers = data['data'].get('subscribers', 'ERROR')
                    nsfw = data['data'].get('over18', 'ERROR')
                    description = data['data'].get('public_description', 'ERROR')
                    status = data['data'].get('subreddit_type', 'ERROR')
                    description = description.replace(",", "").replace("\n", "")
                    if len(description) > MAX_DESC_LEN:
                        description = description[0:MAX_DESC_LEN - 1]
                    if not description:
                        description = ' '
                    record = f'{subreddit},{subscribers},{nsfw},{description},{status}\n'
                    with open(target, 'a', encoding='utf-8') as file:
                        file.write(record)
                        print(f'[+] (#{count}): added record for \'r/{subreddit}\'')
                        count += 1
                    break
                else:
                    print(f'[!] Error: could not fetch data for \'r/{subreddit}\'')
            except requests.exceptions.RequestException as e:
                print(f'[!] Error: {e}')
                if attempt == MAX_RETRIES:
                    subscribers, nsfw, description, status = 'ERROR', 'ERROR', 'ERROR', 'ERROR'
                    record = f'{subreddit},{subscribers},{nsfw},{description},{status}\n'
                    with open(target, 'a', encoding='utf-8') as file:
                        file.write(record)
                    break
        if i % PAUSE_INTERVAL == 0:
            time.sleep(1)
        if count == MAX_RECORDS_PER_FILE:
            target = f'./{datetime.now().isoformat()}{OUT_FILE_SUFFIX}'
            with open(target, 'w', encoding='utf-8') as file:
                file.write('Subreddit,Subscribers,NSFW,Description,Status\n')
            count = 1

if __name__ == '__main__':
    main()
