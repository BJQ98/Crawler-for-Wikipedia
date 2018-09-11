from bs4 import BeautifulSoup
import requests
import re
import threading
import queue

category_queue = queue.Queue()
item_queue = queue.Queue()
start_item = {'title': '', 'url': "https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95"}
category_queue.put(start_item)
old_url_list = set()


# 解析分类和词条url
class CrawlThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

    def run(self):
        global category_queue
        global item_queue
        global old_url_list
        while category_queue:
            cur_item = category_queue.get()
            cur_url = cur_item['url']
            pre_title = cur_item['title']
            resp = requests.get(cur_url).content
            soup = BeautifulSoup(resp, 'html.parser')
            title = soup.find('h1').get_text()
            for _category in soup.find_all('a', {"href": re.compile("^(/wiki/Category).*")}):
                parse_category = "https://zh.wikipedia.org" + _category.get('href')
                item = dict()
                item['title'] = pre_title + title + '-'
                item['url'] = parse_category
                if parse_category not in old_url_list:
                    with self.lock:
                        old_url_list.add(parse_category)
                        category_queue.put(item)
            for _item in soup.find_all('a', {'href': re.compile("^(/wiki/%).*")}):
                parse_item = "https://zh.wikipedia.org" + _item.get('href')
                item = dict()
                item['title'] = pre_title + title + '-'
                item['url'] = parse_item
                if parse_item not in old_url_list:
                    with self.lock:
                        old_url_list.add(parse_item)
                        item_queue.put(item)


# 词条解析线程
class ParserThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

    def run(self):
        global item_queue
        while item_queue:
            cur_item = item_queue.get()
            item_url = cur_item['url']
            pre_title = cur_item['title']
            resp = requests.get(item_url).content
            with self.lock:
                soup = BeautifulSoup(resp, 'html.parser')
                title = soup.find('h1').get_text()
                print(pre_title + title + ':' + item_url)
                fp = open(r'data.txt', 'a', encoding='utf-8')
                fp.write(pre_title + title + ':' + item_url + '\n')
                fp.close()


plist = []
clist = []

for i in range(30):
    p = CrawlThread()
    plist.append(p)
    c = ParserThread()
    clist.append(c)

for i in plist:
    i.start()

for i in clist:
    i.start()

