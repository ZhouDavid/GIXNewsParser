import os
from bs4 import BeautifulSoup
import requests
import json

website_url = 'http://gix.tsinghua.edu.cn/'
language = 'english'
raw_page_path = './raw_html/'+language+'/'
json_output_path = './json/'+language+'/'
img_output_path = './image/'

def download_photo(soup):
    img_urls = soup.find_all('img')
    for img_url in img_urls:
        img_url = img_url.get('src')
        img_url = website_url+img_url[img_url.find('/images'):]
        img_name = img_url.split('/')[-1]
        img = requests.get(img_url).content
        print('image:%s downloaded' % img_name)
        with open(img_output_path+img_name,'wb') as f:
            f.write(img)
            f.close()
    
def convert(html):
    """
    convert raw html to json object:
    story:str, caption:str, photo_urls:list, time:str
    """
    soup = BeautifulSoup(html,'lxml')
    caption = soup.h1.getText()
    content = soup.find('div',{'class':'articlecontent width1000'}).getText()
    time = soup.find('div',{'class':'time'}).getText()
    img_urls = soup.find_all('img')
    img_uris = []
    for img_url in img_urls:
        img_url = img_url.get('src')
        img_url = website_url+img_url[img_url.find('/images'):]
        img_uris.append('./image/'+img_url.split('/')[-1])

    return {
        'caption':caption,
        'content':content,
        'time':time,
        'image_uris':img_uris,
    }
    
    
    

if __name__ == "__main__":
    # load html content
    for file_name in os.listdir(raw_page_path):
        file_path = raw_page_path+file_name
        with open(file_path,'r',encoding='utf-8') as f:
            page_html = f.read()
            f.close()
            json_obj = convert(page_html)
            ff = open (json_output_path+file_name.replace('html','json').replace(' ',''),'w+',encoding='utf-8')
            json.dump(json_obj,ff,ensure_ascii=False)
    