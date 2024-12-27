import requests
from bs4 import BeautifulSoup
import os
import random
import re
from time import sleep

def tiebaPage2PostIDs(tieba_name, page_no):
    url = 'https://tieba.baidu.com/f?kw=' + tieba_name + '&ie=utf-8&pn=' + str((page_no-1)*50)
    try:
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
    except:
        print("网络连接出现了错误，正在重试")
        return
    tags = soup.find_all('a', class_='j_th_tit')
    postIDs = []
    for tag in tags:
        postIDs.append(tag['href'][3:])
    return postIDs
             
def PostID2Text(post_id, page_no):
    url = 'https://tieba.baidu.com/p/' + post_id + '?pn=' + str(page_no)
    try:
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
    except:
        print("网络连接出现了错误，正在重试")
        return
    tags = soup.find_all('div', class_=re.compile('.*d_post_content.*j_d_post_content.*'))
    text = ""
    for tag in tags:
        text += tag.text.strip()
    return text
    
def TextQuantityCount(tieba_name):
    # 定义 corpus 文件夹路径
    corpus_path = os.path.join('corpus', tieba_name)

    # 检查该目录是否存在
    if not os.path.exists(corpus_path):
        return 0

    total_chars = 0  # 用于累加总字符数

    # 遍历该目录下的所有文件夹和文件
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 读取文件并计算字符数
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                total_chars += len(content)  # 累加字符数

    return total_chars

def fetch_tasks():
    # 假设任务文件存储在 crawler_tasks.txt
    task_file = 'crawler_tasks.txt'
    
    # 用一个字典来保存任务
    tasks = {}

    # 打开并读取文件
    with open(task_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 先去除行首尾的空白字符，再按照空格分隔
            parts = line.strip().split()
            
            # 如果分割后的 parts 长度为 2，说明格式正确
            if len(parts) == 2:
                tieba_name = parts[0]  # 贴吧名称
                try:
                    word_count = int(parts[1])  # 字数要求，转换为整数
                    tasks[tieba_name] = word_count
                except ValueError:
                    pass

    return tasks

def is_already_fetched(tieba_name, post_id):
    file_path = os.path.join(os.getcwd(), 'corpus', tieba_name, f'{post_id}.txt')
    return os.path.exists(file_path)


def clean_text(text):
    # 使用正则表达式匹配所有中文字符
    chinese_only = re.findall(r'[\u4e00-\u9fff]+', text)
    # 将匹配到的所有中文字符列表合并成一个字符串
    cleaned_text = ''.join(chinese_only)
    return cleaned_text


def save_text(text, tieba_name, post_id):
    # 保存text，如果不存在tieba_name的目录会自动生成
    directory = os.path.join(os.getcwd(), 'corpus', tieba_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{post_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
     
if __name__ == '__main__':
    
    task_list = fetch_tasks()
    
    # 逐个任务进行完成
    for tieba_name in task_list.keys():
        
        print("开始爬取" + tieba_name + "吧的帖子")
        
        # 统计该贴吧已爬取的中文字符总数
        total_chars = TextQuantityCount(tieba_name)
        
        while total_chars < task_list[tieba_name]:
            
            # 随机从1-200选一页进行爬取
            page_no = random.randint(1, 200)
            post_ids = tiebaPage2PostIDs(tieba_name, page_no)
            
            # 通过减缓爬虫速度防止被贴吧反爬虫
            # sleep(random.randint(15,20))
            
            print("已爬取" + tieba_name + "第" + str(page_no) + "页的所有帖子的id/url")
            
            if post_ids == None or len(post_ids) == 0:
                print('该贴吧页为空，请检查网络问题，以及是否爬虫速度过快被封')
                continue
            
            # 爬取该页的所有帖子
            for post_id in post_ids:
                
                # 跳过已经爬过的帖子
                if is_already_fetched(tieba_name, post_id):
                    print(tieba_name + '吧的帖子' + post_id + '已经爬取过了， 跳过')
                    continue
                
                print('开始爬取' + tieba_name + '吧的帖子' + post_id)
            
                last_text = ""
                all_text = ""
                
                # 枚举第1到第10页
                for i in range(1,11):
                    
                    # 通过减缓爬虫速度防止被贴吧反爬虫
                    # sleep(random.randint(15,20))
                    
                    print('开始爬取第' + str(i) + '页')
                    
                    # 获取此页文本
                    text = PostID2Text(post_id, i)
                    
                    # 判断页号是否超过该帖子总页数，超过的话贴吧默认会返回最后一页
                    if text != last_text and text != None and len(text) > 0:
                        print('成功爬取第' + str(i) + '页')
                        all_text += clean_text(text)
                        last_text = text
                    else:
                        break
                
                if len(all_text) > 0:
                    print('成功爬取' + tieba_name + '吧的帖子' + post_id)
                    
                    save_text(all_text, tieba_name, post_id)
                    
                    total_chars += len(all_text)
                    
                    print(tieba_name + "吧当前已爬取总字数：" + str(total_chars))
                    
                    if total_chars >= task_list[tieba_name]:
                        break
                else:
                    print('该帖子抓取内容为空，请检查网络问题，以及是否爬虫速度过快被封')
            
                
                