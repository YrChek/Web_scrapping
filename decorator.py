import requests
import bs4
import os
import re
import datetime


def log_size(size):
    time = str(datetime.datetime.now())
    path_folder = os.path.join(f'{os.getcwd()}', 'Новая')
    path_file = os.path.join(path_folder, 'Logs.txt')
    path_init = os.path.join(path_folder, '__init__')
    count = 0
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
        with open(path_file, 'w') as file:
            pass
        with open(path_init, 'w') as file:
            pass
    else:
        with open(path_file) as file:
            for i in file:
                count += 1
    text = f'количество записей: {count}'
    if count > size:  # Жесткий контроль количества записей делать не стал, чтобы вся сессия в лог файле осталась.
        del_line = count - size
        with open(path_file) as file:
            data = file.readlines()[del_line:]
        with open(path_file, 'w') as file:
            file.writelines(data)
        data = ''
        text = f'удалено {del_line} записей'
    old_text = f'{time[:19]}, функция "{log_size.__name__}", установленное количество записей: {size}, ' \
               f'результат: {text}\n'
    with open(path_file, 'at') as file:
        file.write(old_text)

    def wrapper(some_function):
        base_url = 'https://habr.com'
        url = base_url + '/ru/all/page1/'
        path = f'{os.getcwd()}/Новая'

        def scrapping(*args):
            time = str(datetime.datetime.now())
            start_time = time[:19]
            result = some_function(*args)
            response = requests.get(url, headers=result)
            time = str(datetime.datetime.now())
            stop_time = time[:19]
            response.raise_for_status()
            res_status = response.status_code
            old_text = f'{start_time}, функция "{scrapping.__name__}", запрос по адресу: "{url}", ' \
                       f'ответ в {stop_time}, статус ответа: <{res_status}>\n'
            with open(path_file, 'at') as file:
                file.write(old_text)
            text = response.text
            soup = bs4.BeautifulSoup(text, features='html.parser')
            articles = soup.find_all("article")
            for article in articles:
                snippet = article.find(class_="tm-article-snippet")
                try: # Хабр какие-то мегапосты начал вставлять с другими тэгами. Сейчас задача другая - поставил исключение.
                    snippet_text = snippet.text
                except:
                    print('Блок мегапост')
                    continue
                art_time = str(article.find("time"))
                title = article.find(class_="tm-article-snippet__title-link")
                title = title.text
                href = article.find(class_="tm-article-snippet__title-link").attrs['href']
                link = base_url + href
                match = True
                for name in args:
                    search_name = re.search(name, snippet_text, flags=re.I)
                    if search_name is not None:
                        match = False
                        res = f'{art_time[49:59]} "{title}" {link}'
                        print(res)
                        time = str(datetime.datetime.now())
                        list_x = [i for i in args]
                        old_text = f'{time[:19]}, функция "{scrapping.__name__}", параметры: {list_x},' \
                                   f' адрес: "{url}",  результат: {res}\n'
                        with open(path_file, 'at') as file:
                            file.write(old_text)
                        break
                if match:
                    time = str(datetime.datetime.now())
                    start_time = time[:19]
                    response = requests.get(link, headers=result)
                    time = str(datetime.datetime.now())
                    stop_time = time[:19]
                    response.raise_for_status()
                    res_status = response.status_code
                    old_text = f'{start_time}, функция "{scrapping.__name__}", запрос по адресу: "{link}",' \
                               f' ответ в {stop_time}, статус ответа: <{res_status}>\n'
                    with open(path_file, 'at') as file:
                        file.write(old_text)
                    content = response.text
                    soup = bs4.BeautifulSoup(content, features='html.parser')
                    post_content = soup.find(id="post-content-body")
                    post_content = post_content.text
                    for name in args:
                        search_name = re.search(name, post_content, flags=re.I)
                        if search_name is not None:
                            res = f'{art_time[49:59]} "{title}" {link}'
                            print(res)
                            time = str(datetime.datetime.now())
                            list_x = [i for i in args]
                            old_text = f'{time[:19]}, функция "{scrapping.__name__}", параметры: {list_x},' \
                                       f' адрес: "{link}",  результат: {res}\n'
                            with open(path_file, 'at') as file:
                                file.write(old_text)
                            break
            return result

        return scrapping

    return wrapper


@log_size(20)
def start(*args):
    time = str(datetime.datetime.now())
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/39.0.2171.95 Safari/537.36'}
    list_x = [i for i in args]
    old_text = f'{time[:19]}, функция "start", параметры: {list_x}, ответ: {HEADERS}\n'
    path = os.path.join(f'{os.getcwd()}', 'Новая', 'Logs.txt')
    with open(path, 'at') as file:
        file.write(old_text)
    return HEADERS


if __name__ == '__main__':
    start('python', 'дизайн', 'фото', 'web')
