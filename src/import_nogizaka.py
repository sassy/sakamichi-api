# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
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
            ret.append(kanji)
    return ret
            

def main():
    Base.metadata.create_all(bind=ENGINE)
    ret = namelist()
    for elem in ret:
        member = NogizakaMemberTable()
        member.name = elem
        session.add(member)
        session.commit()

if __name__ == '__main__':
    main()