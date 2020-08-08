# -*- coding: utf-8 -*-

from pydantic import BaseModel
from db import Base
from db import ENGINE
from db import session
from model import NogizakaMemberTable


import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

base_url = 'http://www.nogizaka46.com/member/'

def get_html():
    req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()

def namelist():
    ret = []
    html = get_html()
    soup = BeautifulSoup(html, "html.parser")
    units = soup.find_all("div", {"class": "unit"})
    for unit in units:
        if unit.find('span',  {"class": "main"}) is not None:
            kanji = unit.find('span',  {"class": "main"}).string
            kana = unit.find('span',  {"class": "sub"}).string if unit.find('span',  {"class": "sub"}) is not None else unit.find('span',  {"class": "sub2"}).string
            url = urljoin(base_url, unit.find('a')['href'])
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            next_html = urllib.request.urlopen(req).read()
            soup2 = BeautifulSoup(next_html, "html.parser")
            birthday = soup2.find_all("dd")[0].string
            ret.append({
                "name" : kanji,
                "name_kana" : kana,
                "birthday" : birthday,
            })
    return ret
            

def main():
    session.execute('truncate table {}'.format(NogizakaMemberTable.__table__))
    ret = namelist()
    for elem in ret:
        print(elem)
        member = NogizakaMemberTable()
        member.name = elem["name"]
        member.namekana = elem["name_kana"]
        member.birthday = elem["birthday"]
        session.add(member)
        session.commit()

if __name__ == '__main__':
    main()