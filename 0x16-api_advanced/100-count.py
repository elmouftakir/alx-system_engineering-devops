#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""

import requests

def count_words(subreddit: str, word_list: list, after: str = '', word_dict: dict = {}):
    """A function that queries the Reddit API, parses the title of all hot articles, 
    and prints a sorted count of given keywords (case-insensitive, delimited by spaces.
    Javascript should count as javascript, but java should not).
    If no posts match or the subreddit is invalid, it prints nothing.
    """

    if not word_dict:
        for word in word_list:
            if word.lower() not in word_dict:
                word_dict[word.lower()] = 0

    if after is None:
        sorted_word_dict = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_word_dict:
            if count:
                print('{}: {}'.format(word, count))
        return None

    url = 'https://www.reddit.com/r/{}/hot/.json'.format(subreddit)
    headers = {'user-agent': 'redquery'}
    parameters = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=parameters, allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        posts = response.json()['data']['children']
        after = response.json()['data']['after']
        for post in posts:
            title = post['data']['title']
            lower = [word.lower() for word in title.split(' ')]

            for word in word_dict.keys():
                word_dict[word] += lower.count(word)

    except Exception:
        return None
    
    count_words(subreddit, word_list, after, word_dict)
