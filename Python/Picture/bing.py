# -*- coding:utf-8 -*-
import urllib.request
import datetime

# @brief  打开网页
# url : 网页地址
# @return 返回网页数据
def open_url(url):
    # 根据当前URL创建请求包
    req = urllib.request.Request(url)
    # 添加头信息，伪装成浏览器访问
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    # 发起请求
    response = urllib.request.urlopen(req)
    # 返回请求到的HTML信息
    return response.read()
# 找图片
def find_picture_url(http_response):
# 查找当前页面所有图片的URL
    http_response = http_response.decode('utf-8')
    img_addrs = []
    # 找图片
    a = http_response.find('<url>')
    #不带停，如果没找到则退出循环
    while a != -1:
        # 以a的位置为起点，找以jpg结尾的图片
        b = http_response.find('</url>', a, a+255)
        # 如果找到就添加到图片列表中
        if b != -1:
            img_addrs.append(http_response[a+5:b])
        # 否则偏移下标
        else:
            b = a + 5
        # 继续找
        a = http_response.find('<url>', b)
    return img_addrs
# url 拼接
def url_joint(picture_url):
    return "http://cn.bing.com/" + picture_url
# @brief 保存图片
# url : 图片url
# addr  : 保存的地址
def save_picture(url,addr):
    with open(addr, 'wb') as f:
        img = open_url(url_joint(url))
        if img:
            f.write(img)
    print("图片已保存")
    return
i = 0
while i < 10:
    i += 1
    # [1] 打开网页
    temp_str = "http://cn.bing.com/HPImageArchive.aspx?format=xml&idx=%d&n=100" % (i)
    response = open_url(temp_str)
    # [2] 找到图片
    list_picture = find_picture_url(response)
    local_time = datetime.datetime.now().microsecond
    j = 0
    # [3] 保存图片
    for picture_url in list_picture:
        j += 1
        local_time_file_name = str(local_time) + str(j) + ".jpg"
        print(local_time_file_name)
        save_picture(picture_url, local_time_file_name)