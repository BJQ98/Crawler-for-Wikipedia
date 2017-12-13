from bs4 import BeautifulSoup
from urllib import request
import re


class SpiderMain(object):
    def __init__(self):
        self.new_urls = []   #初始化各属性为空
        self.old_urls = []
        self.str = []

    def search(self, url):  #找到当前url的所有满足条件的分支
        html = request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        list1 = soup.find('div', {"class": "mw-category-generated"}).find_all('a', {"href": re.compile("^(/wiki/).*")})
        return list1

    def urlcat(self, url):          #拼接成完整url
        page = "https://zh.wikipedia.org"
        newurl = request.urljoin(page, url)
        return newurl

    def title(self, url):            #找到当前url的标题
        newurl = request.urlopen(url)
        soup = BeautifulSoup(newurl, 'html.parser')
        name = soup.find('h1').get_text()
        return name

    def isCategory(self, url):          #是否为目录，不是的话就是词条
        judge = '/wiki/Category:'
        if(url.find(judge)!= -1):
            return True
        else:
            return False

    def write(self, str, url):          #追加方式写入文件
        fout = open(r'C:\Users\lenovo\Desktop\data.txt', 'a', encoding='utf-8')
        fout.write("-".join(self.str) + url+'\n')
        fout.close()

    def Craw(self):                     #爬虫主程序，深度优先搜索思想
        while self.new_urls:
            try:
                count = 0               #准备计数
                list2 = self.search(self.new_urls[-1])
                for url in list2:
                    url = self.urlcat(url.get('href'))    #拼接成完整url
                    if url not in self.old_urls:            #判断是否搜索过
                        if self.isCategory(url):
                            self.str.append(self.title(url))     #分类目录入栈
                            self.new_urls.append(url)
                            break
                        else:
                            self.str.append(self.title(url))
                            print("-".join(self.str), url)      #实现目录-目录格式输出
                            self.write(self.str, url)     #数据存入txt文件
                            self.str.pop()
                            self.old_urls.append(url)
                            count += 1     #找到词条节点开始计数
                            break
                    else:
                        count += 1
                        continue
                if(count == len(list2)):            #若已经遍历当前所有底层分支
                    self.str.pop()                     #各数据出栈
                    self.old_urls.append(self.new_urls[-1])
                    self.new_urls.pop()
            except AttributeError:      #异常处理
                continue
if __name__ == '__main__':
    obj = SpiderMain()
    html = request.urlopen("https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95")
    soup = BeautifulSoup(html, 'html.parser')
    listmain = soup.find_all('p')[5].find_all('a')   #找到自然科学有关
    for b in listmain:
        page = "https://zh.wikipedia.org"
        newurl = request.urljoin(page, b.get('href'))
        obj.new_urls.append(newurl)
        obj.str.append(obj.title(newurl))
        obj.Craw()




