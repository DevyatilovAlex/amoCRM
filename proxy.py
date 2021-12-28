import os
import re
import time
import json
import base64
import random
import requests
import colorama
from pprint import pprint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


HEADERS = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Upgrade-Insecure-Requests': '1',
}


def print_err(message):
    colorama.init(autoreset=True)
    print(colorama.Fore.RED + '[ERROR]:', message)


def create_session(headers, timeout):
    def wrapper(url):
        response_text = ''
        try:
            response = wrapper.session.get(url, headers=headers, timeout=timeout)
            if response.status_code == requests.codes.ok:
                response_text = response.text
        except requests.exceptions.RequestException as request_err:
            print_err(request_err)

        return response_text

    wrapper.session = requests.Session()
    return wrapper


def decode_ip(tag_with_ip):
    script_js = tag_with_ip.script.text
    regular_expression = r'decode\(\"(.*)\"\)'
    encoded_ip_address_match = re.search(regular_expression, script_js)
    if encoded_ip_address_match:
        encoded_ip_address = encoded_ip_address_match[1]
        return base64.b64decode(encoded_ip_address).decode()


def get_proxy(markup):
    proxy_list = []
    bs = BeautifulSoup(markup, 'lxml')
    find_set_tr = bs.find('table', id='proxy_list').find('tbody').find_all('tr')
    for tr in find_set_tr:
        values_first_three_columns_of_row = tr.contents[:3]
        if len(values_first_three_columns_of_row) == 3:
            proxy_list.append({
                'ip_address': decode_ip(values_first_three_columns_of_row[0]),
                'port': values_first_three_columns_of_row[1].text,
                'protocol': values_first_three_columns_of_row[2].text.lower()
            })

    return proxy_list


def parser_proxy(headers, time_sleep=(2, 5), timeout=5):
    proxy_list = []
    pagination_page = 5
    session = create_session(headers, timeout)
    for page in range(1, pagination_page + 1):
        url = f'http://free-proxy.cz/en/proxylist/main/speed/{page}'
        response_text = session(url)
        if response_text:
            new_proxy = get_proxy(response_text)
            proxy_list.extend(new_proxy)

        time.sleep(random.randint(*time_sleep))

    return proxy_list


def save_json(data, file_name='data'):
    if not os.path.exists('data'):
        os.mkdir('data')

    file = f'data/{file_name}.json'
    with open(file, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def generate_proxy(proxy):
    return ('{protocol}://{ip_address}:{port}'.format(**proxy) for proxy in proxy_list)


if __name__ == '__main__':
    proxy_list = parser_proxy(HEADERS)
    save_json(proxy_list)
    pprint(list(generate_proxy(proxy_list)))
