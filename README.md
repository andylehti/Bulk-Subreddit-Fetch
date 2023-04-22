# Bulk-Subreddit-Fetch
Bulk subreddit fetcher to check subreddit name, subscribers, over18, description, and public status.

- Added pauses for x intervals
- Added recheck in case of failure (don't use it unless you suspect error)
- Added ignores in case of errors that stop the script
- Added **reddits.txt** for subreddit search query

**NOTE:** if a subreddit is private, restricted, quarantined, banned, or any other status that will not allow you to view it; it will throw this error:

```[!] Error: could not fetch data for 'r/xxxx```

The script still will grab as much information as it can, despite it saying error.

# How to run

```git clone https://github.com/andylehti/Bulk-Subreddit-Fetch```

```cd Bulk-Subreddit-Fetch```

```nano reddits.txt```

```python3 breddit.py```

## CSV will be exported to same directory
