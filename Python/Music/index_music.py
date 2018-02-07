import xlwt  
import requests  
from bs4 import BeautifulSoup  
import re  

def get_url(url):  
    try:  
        r = requests.get(url)  
        r.raise_for_status()  
        r.encoding = r.apparent_encoding  
        return r.text  
    except:  
        print('wrong!!!!!!!!!!!!!')  
def singer_url(url):  
    #只抓取前10位的歌手  
    html = get_url(url)  
    soup = BeautifulSoup(html,'html.parser')  
    top_10 = soup.find_all('div',attrs = {'class':'u-cover u-cover-5'})  
    singers = []  
    for i in top_10:  
        singers.append(re.findall(r'.*?<a class="msk" href="(/artist\?id=\d+)" title="(.*?)的音乐"></a>.*?',str(i))[0]) #问号有问题  
        #解析的代码和源代码的顺序不同，在用正则表达式的时候要注意  
    song_info(singers)  
def song_info(singers):  
    url = 'http://music.163.com'    
    for singer in singers:  
        try:  
            new_url = url + str(singer[0])  
            songs = get_url(new_url)  
            soup = BeautifulSoup(songs,'html.parser')  
            Info = soup.find_all('textarea',attrs = {'style':'display:none;'})[0]  
            songs_url_and_name = soup.find_all('ul',attrs = {'class':'f-hide'})[0]  
            #print(songs_url_and_name)    
            datas = []  
            data1 = re.findall(r'"album".*?"name":"(.*?)".*?',str(Info.text))  
            data2 = re.findall(r'.*?<li><a href="(/song\?id=\d+)">(.*?)</a></li>.*?',str(songs_url_and_name))  
            for i in range(len(data2)):  
                datas.append([data2[i][1],data1[i],'http://music.163.com/#'+ str(data2[i][0])])  
           # print(datas)  
            save_excel(singer,datas)  
        except:  
            continue  
def save_excel(singer,datas):  
    fpath = 'D:/python/网易云数据'  
    book = xlwt.Workbook()  
    sheet1 = book.add_sheet('sheet1',cell_overwrite_ok = True)  
    sheet1.col(0).width = (25*256)  
    sheet1.col(1).width = (30*256)  
    sheet1.col(2).width = (40*256)  
    #xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位。  
    #xlwt创建时使用的默认宽度为2960，既11个字符0的宽度  
    #所以我们在设置列宽时可以用如下方法：  
    #width = 256 * 20    256为衡量单位，20表示20个字符宽度  
    heads = ['歌曲名称','专辑','歌曲链接']  
    count = 0   
    print('正在存入文件......')  
    for head in heads:  
        sheet1.write(0,count,head)  
        count += 1   
    i = 1  
    for data in datas:  
        j = 0  
        for k in data:  
            sheet1.write(i,j,k)  
            j += 1  
        i += 1  
    book.save(fpath + str(singer[1]) + '.xls')#括号里写存入的地址  
    print('OK！')  
def main():  
    url = 'http://music.163.com/discover/artist/cat?id=1002'#华语男歌手页面  
    singer_url(url)  
main()