from requests import get
from urllib.parse import urlparse
from django.conf import settings


def is_shorten_url(url):
    return 'vk.cc' in url


def get_shortened_link(url):
    token = settings.VK_API_TOKEN
    payload = {'v': '5.236', 'access_token': token, 'url': url}
    response = get(
        'https://api.vk.ru/method/utils.getShortLink',
        params=payload
    )
    response.raise_for_status()
    if not response.json().get('response'):
        return 'error'
    short_url = response.json()['response']['short_url']
    return short_url


def get_link_click_count(url):
    if 'vk.cc' not in url:
        return 0
    token = settings.VK_API_TOKEN
    parsed_url = urlparse(url).path.lstrip('/')
    payload = {
        'v': '5.236',
        'access_token': token,
        'key': parsed_url,
    }
    response = get('https://api.vk.ru/method/utils.getLinkStats',
                            params=payload)
    response.raise_for_status()
    if response.json().get('response') and len(response.json()['response']['stats']) > 0:
        click_count = response.json()['response']['stats'][0]['views']
    else:
        click_count = 0
    return click_count
