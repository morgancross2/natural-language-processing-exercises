import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_blog_article_content(art):
    output = {}
    output['headline'] = art.find('h2').text.strip()
    output['posted'] = art.find_all('p')[0].text.strip()
    output['content'] = art.find_all('p')[1].text.strip()
    return output

def get_blog_articles(url):
    headers = {'User-Agent': 'Codeup Data Science'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    arts = soup.select('article')
    final = [get_blog_article_content(art) for art in arts]
    return pd.DataFrame(final)

def get_news_article_content(url, page):
    temp = {}
    soup = BeautifulSoup(requests.get(url+page).content, 'html.parser')
    headers = soup.select('a.clickable')
    contents = soup.select('div.news-card-content.news-right-box')
    titles = [title.span.text.strip() for title in headers]
    arts = [art.div.text.strip() for art in contents]
    temp['title'] = titles
    temp['content'] = arts
    temp['category'] = page.strip('/')
    return pd.DataFrame(temp)

def get_news_articles(url):
    pages = ['/business', '/sports', '/technology', '/entertainment']
    results = pd.DataFrame()
    for page in pages:
        hold = get_news_article_content(url, page)
        results = pd.concat([results, hold])
    return results