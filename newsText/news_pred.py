import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
django.setup()
import newsText.models as nm

def news_pred(SeaNews):
    # 将数据库的所有内容读取下来，按照QuerySet的格式储存，需要用.values()来查询。
    news_list = SeaNews.objects.all()
    news_list2 = list(news_list.values("news_content"))
    news_list_content = []
    # 把内容存入news_list_content
    for dict_ in news_list2:
        news_list_content.append(dict_['news_content'])
    # 去\xa0\
    # news_list3.replace('\xa0', '')
    # 载入停用词 按行读取 rstrip去掉换行符 'r':只读  lower() 方法转换字符串中所有大写字符为小写。
    stopwords = set()
    with open('static/data/stopwords.txt', 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.rstrip('\n')
            if line:
                stopwords.add(line.lower())
    # tfidf训练
    tfidf = TfidfVectorizer(tokenizer=jieba.lcut, stop_words=stopwords,
                            min_df=50, max_df=0.3)
    x = tfidf.fit_transform(news_list_content)
    tFIDFDataFrame = pd.DataFrame(x.toarray())
    # 获取词袋模型中的所有词语（格式为list) ,作为数据框的columns
    tFIDFDataFrame.columns = tfidf.get_feature_names()
    # 输出列均值，即关键词的tfidf均值
    keyword_score = tFIDFDataFrame.mean()
    keyword_score_dic = keyword_score.to_dict()
    # 遍历文章 计算得分
    article_score = {}
    for i, article in enumerate(news_list_content):
        score = 0
        for keyword in keyword_score_dic:
            if article.find(keyword) != -1:
                score += keyword_score_dic[keyword]
        article_score[i] = score
    score_list = []
    for score in article_score:
        score_list.append(article_score[score])
    # 把得到的分数存进数据库
    for j in range(1, len(score_list)):
        k = SeaNews.objects.get(id=j)
        k.news_score = score_list[j-1]
        k.save()
# 传入一个models的文件就能使用了
news_pred(nm.SeaNewsCbhgV2)
news_pred(nm.SeaNewsCultureV2)
news_pred(nm.SeaNewsDomesticV2)
news_pred(nm.SeaNewsEconomicsV2)
news_pred(nm.SeaNewsEduV2)
news_pred(nm.SeaNewsInternationalV2)
news_pred(nm.SeaNewsMilV2)
news_pred(nm.SeaNewsTechV2)
news_pred(nm.SeaNewsTodayhotV2)
news_pred(nm.SeaNewsTraveV2)