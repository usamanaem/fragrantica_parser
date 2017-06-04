# -*- coding: utf-8 -*-
import csv
import logging
from lxml import html
import re
import requests
import urllib.parse

ROOT_URL = 'https://www.fragrantica.ru'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
RE_NAMESPACE = {'re': "http://exslt.org/regular-expressions"}


def get_list_groups():
    url = urllib.parse.urljoin(ROOT_URL, 'groups/')
    r = requests.get(url, headers=HEADERS)
    tree = html.fromstring(r.content)
    return {gr.text_content(): gr.get('href') for gr in tree.xpath('//span/a[re:test(@href, "^/groups.*.html$")]',
                                                namespaces=RE_NAMESPACE)}


def get_list_fragrances_by_group(group_path):
    url = urllib.parse.urljoin(ROOT_URL, group_path)
    r = requests.get(url, headers=HEADERS)
    tree = html.fromstring(r.content)
    return [fr.get('href') for fr in tree.xpath('//a[re:test(@href, "^/perfume.*.html$")]',
                                                namespaces=RE_NAMESPACE)]


def get_fragrance_data(fragrance_path):
    url = urllib.parse.urljoin(ROOT_URL, fragrance_path)
    r = requests.get(url, headers=HEADERS)
    tree = html.fromstring(r.content)
    fragrance = {}
    try:
        designer = tree.xpath('//div[@class="subTtl"]/a/text()', namespaces=RE_NAMESPACE)[0]
        match = re.match(r"(?P<title>.*?) %s( для (?P<gender>.*?))?$" % designer,
                         tree.xpath('//h1/span[@itemprop="name"]/text()')[0])
        if match:
            fragrance = match.groupdict()
        fragrance['designer'] = designer
        fragrance['pic'] = tree.xpath('//div[@id="mainpicbox"]/img/@src')[0]
        fragrance['noses'] = tree.xpath('//a[re:test(@href, "^.*/noses.*.html$")]/b/text()', namespaces=RE_NAMESPACE)
        fragrance['description'] = tree.xpath('//div[@itemprop="description"]')[0].text_content().strip()
        match = re.match(r".* выпущен в (?P<year>.*?)\.", fragrance['description'])
        fragrance['year'] = match.group('year') if match else ''
        for note in tree.xpath('//*[re:test(., "^(верхние Ноты|средние Ноты|база Ноты|Ноты Аромата)$")]', namespaces=RE_NAMESPACE):
            fragrance[note.text_content()] = note.xpath(
                '../span[@class="rtgNote"]/img/@alt|../*/span[@class="rtgNote"]/img/@alt')
        fragrance['comments'] = tree.xpath('count(//div[@class="pwq"])')
        #print(fragrance)
    except IndexError:
        logging.warning(fragrance_path)
    return fragrance


def group_import_csv(name, group_path):
    keys = (['title', 'description', 'gender', 'designer', 'pic', 'noses', 'year', 'Ноты Аромата', 'верхние Ноты',
             'средние Ноты', 'база Ноты', 'comments'])
    with open(name + '.csv', 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        for fr in get_list_fragrances_by_group(group_path):
            w.writerow(get_fragrance_data(fr))


list_groups = get_list_groups()
for name, path in list_groups.items():
    group_import_csv(name, path)
