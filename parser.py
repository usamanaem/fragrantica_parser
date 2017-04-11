import requests
import urllib.parse
from lxml import html


ROOT_URL = 'https://www.fragrantica.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}


def get_groups():
    url = urllib.parse.urljoin(ROOT_URL, 'groups/')
    r = requests.get(url, headers=HEADERS)
    tree = html.fromstring(r.content)
    return [group.get('href') for group in tree.xpath('//a[re:test(@href, "^/groups.*.html$")]',
                                                      namespaces={'re': "http://exslt.org/regular-expressions"})]


list_groups = get_groups()
