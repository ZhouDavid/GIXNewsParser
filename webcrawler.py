import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

website_url = "http://gix.tsinghua.edu.cn/Home/news/"
download_path = './raw_html/english/'

def getPageUrls(website_url):
    print('loading front page urls....')
    homepage_html = requests.get(website_url).text
    print('parsing front page html')
    soup = BeautifulSoup(homepage_html,'lxml')
    pager = soup.find('div',{'class':'pager'})
    page_urls = set()
    for linker in pager.find_all('a'):
        link = website_url + linker.get('href')
        print('page link:%s added' % link)
        page_urls.add(link)
    return list(page_urls)


def getContentUrls(list_page_url):
    print('loading page:%s' % list_page_url)
    list_page_html = requests.get(list_page_url).text
    print('parsing page:%s' % list_page_url)
    soup = BeautifulSoup(list_page_html,'lxml')
    content_linkers = soup.find('ul',{'class':'clearfix'}).find_all('li')
    content_urls = set()
    for content_linker in content_linkers:
        link = website_url + content_linker.find('a').get('href')
        print('content link:%s added' % link)
        content_urls.add(link)
    return list(content_urls)


def getHTML(content_url):
    r = requests.get(content_url)
    r.encoding = 'utf-8'
    content_html = r.text
    return content_html

def downloadHTML(content, write_path):
    soup = BeautifulSoup(content,'lxml')
    title = soup.h1.getText()
    time = soup.find('div',{'class':'time'}).getText()
    print(title,time)
    with open(write_path+time+'.html','w+', encoding='utf-8') as f:
        print('downloading page: %s-%s' % (title,time))
        f.write(content)
        f.close()
    

if __name__ == "__main__":
    front_page_urls = getPageUrls(website_url)
    print(front_page_urls)
    content_urls = []
    for front_page_url in tqdm(front_page_urls):
        content_urls.extend(getContentUrls(front_page_url))
        
    for content_url in tqdm(content_urls):
        raw_html = getHTML(content_url)
        downloadHTML(raw_html, download_path)


