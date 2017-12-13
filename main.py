from bs4 import BeautifulSoup
from urllib import request
import re


class SpiderMain(object):
    def __init__(self):
        self.new_urls = []   
        self.old_urls = []
        self.str = []

    def search(self, url):  
        html = request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        list1 = soup.find('div', {"class": "mw-category-generated"}).find_all('a', {"href": re.compile("^(/wiki/).*")})
        return list1

    def urlcat(self, url):          
        page = "https://zh.wikipedia.org"
        newurl = request.urljoin(page, url)
        return newurl

    def title(self, url):           
        newurl = request.urlopen(url)
        soup = BeautifulSoup(newurl, 'html.parser')
        name = soup.find('h1').get_text()
        return name

    def isCategory(self, url):         
        judge = '/wiki/Category:'
        if(url.find(judge)!= -1):
            return True
        else:
            return False

    def write(self, str, url):         
        fout = open(r'C:\Users\lenovo\Desktop\data.txt', 'a', encoding='utf-8')
        fout.write("-".join(self.str) + url+'\n')
        fout.close()

    def Craw(self):                     
        while self.new_urls:
            try:
                count = 0             
                list2 = self.search(self.new_urls[-1])
                for url in list2:
                    url = self.urlcat(url.get('href'))    
                    if url not in self.old_urls:           
                        if self.isCategory(url):
                            self.str.append(self.title(url))   
                            self.new_urls.append(url)
                            break
                        else:
                            self.str.append(self.title(url))
                            print("-".join(self.str), url)    
                            self.write(self.str, url)   
                            self.str.pop()
                            self.old_urls.append(url)
                            count += 1    
                            break
                    else:
                        count += 1
                        continue
                if(count == len(list2)):          
                    self.str.pop()                   
                    self.old_urls.append(self.new_urls[-1])
                    self.new_urls.pop()
            except AttributeError:    
                continue
if __name__ == '__main__':
    obj = SpiderMain()
    html = request.urlopen("https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95")
    soup = BeautifulSoup(html, 'html.parser')
    listmain = soup.find_all('p')[5].find_all('a')  
    for b in listmain:
        page = "https://zh.wikipedia.org"
        newurl = request.urljoin(page, b.get('href'))
        obj.new_urls.append(newurl)
        obj.str.append(obj.title(newurl))
        obj.Craw()




