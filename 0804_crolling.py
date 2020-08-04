from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re


base_url = 'https://movie.naver.com/movie/running/current.nhn'

URL = requests.get(base_url)

soup = BeautifulSoup(URL.text, 'html.parser')

mov = soup.select(
    'div[id=wrap].basic > div[id=container] > div[id=content] > div.article > div.obj_section > div.lst_wrap > ul.lst_detail_t1 > li > dl.lst_dsc > dt.tit'
)




for a_tag in mov:
    print(a_tag.select_one('a').get_text())
    p = re.compile('[\d+]')
    m = p.findall(a_tag.select_one('a')['href'])
    print(m)
    