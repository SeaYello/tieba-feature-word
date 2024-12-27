import os

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

def read_word_result(tieba_name):

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造目标文件路径
    file_path = os.path.join(current_dir, 'words', f"{tieba_name}.txt")
    
    # 如果文件不存在，返回空字典
    if not os.path.exists(file_path):
        return {}
    
    # 初始化一个空字典存储词频
    word_result = {}
    
    # 逐行读取文件内容并解析
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 按空格分割每行数据
            parts = line.strip().split()
            if len(parts) == 2:  # 确保每行有两个部分：词和词频
                word = parts[0]
                frequency = float(parts[1])  # 将词频转换为浮点数
                word_result[word] = frequency
    
    return word_result

def extract_feature_words(all_word_result):
    
    # 初始化一个字典存储每个词的文档频率（DF）
    document_frequency = {}

    # 遍历每个贴吧的词频数据，统计文档频率
    for tieba_name, word_frequencies in all_word_result.items():
        for word in word_frequencies.keys():
            # 如果该词首次出现，将其文档频率初始化为 0
            document_frequency[word] = document_frequency.get(word, 0) + 1

    # 初始化一个字典存储每个贴吧的特色词
    feature_words = {}

    # 遍历每个贴吧，计算特色度得分并选出前 10 个词
    for tieba_name, word_frequencies in all_word_result.items():
        # 初始化一个列表存储该贴吧的词及其特色度得分
        word_scores = []

        for word, frequency in word_frequencies.items():
            # 获取该词的文档频率
            df = document_frequency[word]
            # 计算特色度得分
            score = frequency / (df ** 4)
            # 将词和得分添加到列表
            word_scores.append((word, score))
        
        # 按得分从大到小排序
        word_scores.sort(key=lambda x: x[1], reverse=True)
        # 取前 20 个词的词语作为该贴吧的特色词
        feature_words[tieba_name] = [word for word, _ in word_scores[:20]]

    return feature_words

def save_report(feature_words):

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造报告文件的路径
    report_path = os.path.join(current_dir, 'report.txt')
    
    # 打开文件进行写入（如果文件已存在，会覆盖）
    with open(report_path, 'w', encoding='utf-8') as file:
        for tieba_name, words in feature_words.items():
            # 将特色词汇拼接为一个字符串，用顿号（、）分隔
            words_str = "、".join(words)
            # 写入一行报告内容
            file.write(f"{tieba_name}吧特色词汇：{words_str}。\n\n")
            
def show_report():

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造报告文件的路径
    report_path = os.path.join(current_dir, 'report.txt')
    
    # 检查报告文件是否存在
    if not os.path.exists(report_path):
        print("报告文件 report.txt 不存在。")
        return
    
    # 打开文件读取内容并输出到控制台
    with open(report_path, 'r', encoding='utf-8') as file:
        for line in file:
            print(line.strip())  # 输出每一行内容，去掉末尾多余的换行符

if __name__ == '__main__':
    
    tieba_names = fetch_tieba_names()
    
    all_word_result = {}
    
    for tieba_name in tieba_names:
        word_result = read_word_result(tieba_name)
        all_word_result[tieba_name] = word_result
    
    feature_word_result = extract_feature_words(all_word_result)
    save_report(feature_word_result)
    show_report()