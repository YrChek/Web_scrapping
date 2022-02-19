import requests
import bs4
import re


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
base_url = 'https://habr.com'
url = base_url + '/ru/all/page1/'
KEYWORDS = ['python', 'дизайн', 'фото', 'web']

if __name__ == '__main__':
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all("article")
    for article in articles:
        snippet = article.find(class_="tm-article-snippet")
        snippet_text = snippet.text
        time = str(article.find("time"))
        title = article.find(class_="tm-article-snippet__title-link")
        title = title.text
        href = article.find(class_="tm-article-snippet__title-link").attrs['href']
        link = base_url + href
        match = True
        for name in KEYWORDS:
            search_name = re.search(name, snippet_text, flags=re.I)
            if search_name is not None:
                match = False
                print(f'{time[49:59]} "{title}" {link}')
                break
        if match:
            response = requests.get(link, headers=HEADERS)
            response.raise_for_status()
            content = response.text
            soup = bs4.BeautifulSoup(content, features='html.parser')
            post_content = soup.find(id="post-content-body")
            post_content = post_content.text
            for name in KEYWORDS:
                search_name = re.search(name, post_content, flags=re.I)
                if search_name is not None:
                    print(f'{time[49:59]} "{title}" {link}')
                    break
