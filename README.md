这个项目是本账号拥有者和小组成员在DGUT完成的2024自然语言处理课程的大作业。

项目概要：
每个学校有自己的特色，例如东莞理工学院有“北街”、“知行课”等。我们希望知道每个学校的特色是什么。为了实现这个，我们可以利用贴吧的语料信息：首先选取多个不同学校，然后爬取每个学校的的贴吧内容，代表该学校的语料。接着，对于每个学校的语料，我们使用语言学的统计方法进行无词库抽词，得到该学校的所有词语，以及每个词语的打分信息。最后，我们将设计一个算法对比不同学校的词语信息，选举出每个学校的特色词。

使用方式：
下载项目中的所有文件，然后修改 crawler_tasks.txt 中的内容（表示每个贴吧爬虫的任务要求，按中文字符个数计算）。然后运行 tieba_crawler.py 进行贴吧爬虫（注意切换IP防止被封，但通常封禁后一段时间会解封）。接着运行 words_extract.py，最后运行 feature_word_extract.py 得到最终报告。报告将会被保存在 report.txt 中。

项目实施细节可以在 tieba-feature-word_project_plan.docx 中找到。
