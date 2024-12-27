import os
import math

def fetch_tieba_names():
    # 从已爬取语料的文件夹名称中提取所有贴吧名称
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造 corpus 文件夹路径
    corpus_dir = os.path.join(current_dir, 'corpus')
    
    # 如果 corpus 文件夹不存在，返回空列表
    if not os.path.exists(corpus_dir):
        return []
    
    # 获取 corpus 文件夹下的所有子文件夹名称
    tieba_names = [
        folder_name for folder_name in os.listdir(corpus_dir)
        if os.path.isdir(os.path.join(corpus_dir, folder_name))
    ]
    
    return tieba_names

def read_text(tieba_name):
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tieba_dir = os.path.join(current_dir, 'corpus', tieba_name)
    
    # 如果目标贴吧文件夹不存在，返回空字符串
    if not os.path.exists(tieba_dir) or not os.path.isdir(tieba_dir):
        return ""
    
    # 初始化一个空字符串用于拼接文本内容
    combined_text = ""
    
    # 遍历该贴吧文件夹下的所有文件
    for file_name in os.listdir(tieba_dir):
        file_path = os.path.join(tieba_dir, file_name)
        # 读取文件内容并拼接到 combined_text
        with open(file_path, 'r', encoding='utf-8') as file:
            combined_text += file.read()
    
    return combined_text

# 给定左邻字或右邻字列表，计算信息熵
def calc_entropy(char_list):
    
    count = {}
    for char in char_list:
        count[char] = count.get(char, 0) + 1
        
    entropy = 0
    for cnt in count.values():
        freq = cnt/len(char_list)
        entropy -= freq*math.log2(freq)
        
    return entropy

def save_result(tieba_name, result):
    
    # 保存词频分析结果到指定贴吧对应的文本文件中

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造 words 文件夹路径
    words_dir = os.path.join(current_dir, 'words')
    
    # 如果 words 文件夹不存在，创建该文件夹
    if not os.path.exists(words_dir):
        os.makedirs(words_dir)
    
    # 构造目标贴吧的文件路径
    file_path = os.path.join(words_dir, f"{tieba_name}.txt")
    
    # 将词频结果写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, frequency in result.items():
            # 每行写入词和对应的词频，以空格分隔
            file.write(f"{word} {frequency:.8f}\n")

def extract_words(text):
    
    n = len(text)
    frequency = {}
    left_chars = {}
    right_chars = {}
    
    for i in range(1, 5):
        for j in range(1, n-i):
            word = text[j:j+i]
            frequency[word] = frequency.get(word, 0) + 1
            left_chars.setdefault(word, []).append(text[j-1])
            right_chars.setdefault(word, []).append(text[j+i])
    
    print("词频和左右邻字预处理完毕，开始抽词")
    
    # 被认为是合法的词语（key是词语，value是词频）
    accepted_words = {}
    
    for word in frequency.keys():
        if len(word) == 1:
            continue
        cohesion = 1e18
        for i in range(1, len(word)):
            left_part = word[0:i]
            right_part = word[i:]
            cohesion = min(cohesion, frequency[word]/frequency[left_part]/frequency[right_part]*n)
        flexibility = min(calc_entropy(left_chars[word]), calc_entropy(right_chars[word]))
        accepted_words[word] = frequency[word] * math.log2(cohesion)**3 * flexibility**3
    
    return accepted_words
    
if __name__ == '__main__':
    
    tieba_names = fetch_tieba_names()
    
    for tieba_name in tieba_names:
        print("开始对" + tieba_name + "吧的文本进行抽词")
        text = read_text(tieba_name)
        words = extract_words(text)
        print(tieba_name + "吧的文本抽词完毕，共抽出" + str(len(words)) + "个词语")
        save_result(tieba_name, words)