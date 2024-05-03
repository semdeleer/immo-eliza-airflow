from bs4 import BeautifulSoup
import concurrent.futures
import requests
import functools
import pandas as pd
import requests
import time
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def immo_pagelinks():
    """
    Starting from a root_url fetches the immoweb links for n pages

    :param n: number of pages
    :return: list of urls
    """
    immopagelinks=[]
    root_url = "https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page="

    for number in range(1, 3):
        immopagelinks.append(f"{root_url}{number}&orderBy=relevance")

    return immopagelinks

def immo_weblinks():
    root_url = "https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page=2&orderBy=relevance"
    with requests.Session() as session:
        r = session.get(root_url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        ul_element = soup.find('ul', id='content-main', class_='search-results__list')
        return ul_element

    
    for content in cont.find_all("ul", "class:search-results__list"):
        print(content)

def write_to_db_weblinks():
    Base = declarative_base()
    class Weblinks(Base):
        __tablename__ = 'weblink'

        link = Column(String, primary_key=True)
        

    engine = create_engine("postgresql://postgres:mes2102@localhost:5432/immoweb")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    weblinks = multiWeblinks()
    for links in weblinks:
        link = Weblinks(weblink=links)
        session.add(link)
        session.commit()
    print(weblinks)


if __name__ == "__main__":
    m = immo_weblinks()
    
    print(m)