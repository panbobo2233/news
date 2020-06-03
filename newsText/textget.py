#!/user/bin/python
# coding:utf-8
__author__ = 'yan.shi'

import datetime
from datetime import timedelta

import nltk
import numpy
import jieba
import codecs
import pymysql
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from newsText.crawler_total_v2 import main_update

N=100#单词数量
CLUSTER_THRESHOLD=5#单词间的距离
TOP_SENTENCES=5#返回的top n句子 此参数修改过，本来是5

def background_update():
    executors = {
        'default': ThreadPoolExecutor(20)
    }
    scheduler = BackgroundScheduler(executors=executors)
    scheduler.add_job(main_update, "cron", hour=0,minute=15)
    scheduler.start()
background_update()
#
#分句
def sent_tokenizer(texts):
    start=0
    i=0#每个字符的位置
    sentences=[]
    punt_list='.!?。！？'.encode('utf-8').decode('utf8') #',.!?:;~，。！？：；～'.decode('utf8')
    for text in texts:
        if text in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i+1])#当前标点符号位置
            start=i+1#start标记到下一句的开头
            i+=1
        else:
            i+=1#若不是标点符号，则字符位置继续前移
            token=list(texts[start:i+2]).pop()#取下一个字符
    if start<len(texts):
        sentences.append(texts[start:])#这是为了处理文本末尾没有标点符号的情况
    return sentences

#停用词
def load_stopwordslist(path):
    print('load stopwords...')
    stoplist=[line.strip() for line in codecs.open(path,'r',encoding='utf8').readlines()]
    stopwrods={}.fromkeys(stoplist)
    return stopwrods

#摘要
def summarize(text):
    stopwords=load_stopwordslist('newsText/stop_words.txt')
    sentences=sent_tokenizer(text)
    words=[w for sentence in sentences for w in jieba.cut(sentence) if w not in stopwords if len(w)>1 and w!='\t']
    wordfre=nltk.FreqDist(words)
    topn_words=[w[0] for w in sorted(wordfre.items(),key=lambda d:d[1],reverse=True)][:N]
    scored_sentences=_score_sentences(sentences,topn_words)
    #approach 1,利用均值和标准差过滤非重要句子
    avg=numpy.mean([s[1] for s in scored_sentences])#均值
    std=numpy.std([s[1] for s in scored_sentences])#标准差
    mean_scored=[(sent_idx,score) for (sent_idx,score) in scored_sentences if score>(avg+0.5*std)]
    #approach 2，返回top n句子
    top_n_scored=sorted(scored_sentences,key=lambda s:s[1])[-TOP_SENTENCES:]
    top_n_scored=sorted(top_n_scored,key=lambda s:s[0])
    return dict(top_n_summary=[sentences[idx] for (idx,score) in top_n_scored],mean_scored_summary=[sentences[idx] for (idx,score) in mean_scored])

 #句子得分
def _score_sentences(sentences,topn_words):
    scores=[]
    sentence_idx=-1
    for s in [list(jieba.cut(s)) for s in sentences]:
        sentence_idx+=1
        word_idx=[]
        for w in topn_words:
            try:
                word_idx.append(s.index(w))#关键词出现在该句子中的索引位置
            except ValueError:#w不在句子中
                pass
        word_idx.sort()
        if len(word_idx)==0:
            continue
        #对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters=[]
        cluster=[word_idx[0]]
        i=1
        while i<len(word_idx):
            if word_idx[i]-word_idx[i-1]<CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster=[word_idx[i]]
            i+=1
        clusters.append(cluster)
        #对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score=0
        for c in clusters:
            significant_words_in_cluster=len(c)
            total_words_in_cluster=c[-1]-c[0]+1
            score=1.0*significant_words_in_cluster*significant_words_in_cluster/total_words_in_cluster
            if score>max_cluster_score:
                max_cluster_score=score
        scores.append((sentence_idx,max_cluster_score))
    return scores;

def abouttime():
    today = datetime.date.today();
    print(today)
    #本周第一天
    this_week_start = today - timedelta(days=today.weekday())
    print(this_week_start)
    #本周最后一天
    this_week_end = today + timedelta(days=6 - today.weekday())
    print(this_week_end)
    #本月第一天
    this_month_start = datetime.datetime(today.year, today.month, 1)
    print(this_month_start)
    #本月最后一天
    this_month_end = datetime.datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    print(this_month_end)
    re_time=[]
    re_time.append(today.strftime("%Y-%m-%d"))
    re_time.append(this_week_start.strftime("%Y-%m-%d"))
    re_time.append(this_week_end.strftime("%Y-%m-%d"))
    re_time.append(this_month_start.strftime("%Y-%m-%d"))
    re_time.append(this_month_end.strftime("%Y-%m-%d"))
    return re_time


def week_newsGenerate():
    today = datetime.date.today();
    # 本周第一天
    this_week_start = today - timedelta(days=today.weekday())
    # 本周最后一天
    this_week_end = today + timedelta(days=6 - today.weekday())
    #news_week_list  = SeaNews.objects.filter(news_date__range=(this_week_start,this_week_end)).order_by('-news_score')[:10]

def month_newsGenerate():
    today = datetime.date.today();
    # 本月第一天
    this_month_start = datetime.datetime(today.year, today.month, 1)
    # 本月最后一天
    this_month_end = datetime.datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    # news_month_list  = SeaNews.objects.filter(news_date__range=(this_month_start,this_month_end)).order_by('-news_score')[:10]

# if __name__=='__main__':

def mainMethod():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "hellosea")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    # var1 = "SELECT `news_content` FROM sea_news_cbhg WHERE `news_date`>='2020-01-01' \
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_culture` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_domestic` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_economics` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_edu` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_international` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'\
    #         UNION\
    #         SELECT `news_content` FROM `sea_news_mil` WHERE `news_date`>='2020-01-01'\
    #         AND `news_date`<='2020-01-07'"

    var2 = "SELECT `news_content`, news_score FROM sea_news_cbhg_v2 WHERE `news_date`>=%s \
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_culture_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_domestic_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_economics_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_edu_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_international_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_mil_v2` WHERE `news_date`>=%s\
              AND `news_date`<=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_tech_v2` WHERE `news_date`>=%s\
              AND `news_date` <=%s\
              UNION\
              SELECT `news_content`,news_score FROM `sea_news_trave_v2` WHERE `news_date` >=%s\
              AND `news_date` <=%s\
              ORDER BY news_score DESC\
              LIMIT 10"

    var3 = "SELECT `news_content`, news_score FROM sea_news_cbhg_v2 WHERE `news_date`=%s \
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_culture_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_domestic_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_economics_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_edu_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_international_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_mil_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_tech_v2` WHERE `news_date`=%s\
                  UNION\
                  SELECT `news_content`,news_score FROM `sea_news_trave_v2` WHERE `news_date` =%s\
                  ORDER BY news_score DESC\
                  LIMIT 10"



    re_time = abouttime()

    f_week_day = '2020-05-01'
    l_week_day = '2020-05-07'
    f_month_day = '2020-05-01'
    l_month_day = '2020-05-31'
    today_day = '2020-05-27'
    # today_day = datetime.date.today().strftime("%Y-%m-%d")
    # today_day = re_time[0]
    # f_week_day = re_time[1]
    # l_week_day = re_time[2]
    # f_month_day = re_time[3]
    # l_month_day = re_time[4]


    # param = ('2020-01-07','2020-01-14','2020-01-7','2020-01-14','2020-01-7','2020-01-14','2020-01-07','2020-01-14','2020-01-07','2020-01-14','2020-01-07','2020-01-14','2020-01-07','2020-01-14','2020-01-07','2020-01-14','2020-01-07','2020-01-14')
    param = (f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day,f_week_day,l_week_day)
    param1 = (f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day,f_month_day,l_month_day)
    param2 = (today_day,today_day,today_day,today_day,today_day,today_day,today_day,today_day,today_day)


    # cursor.execute(var1)
    cursor.execute(var2,param)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    i = 0
    summarizes_weekly=[]
    for d in data:
        print(d[0])
        summarize_re = summarize(d[0])
        summarizes_weekly.append(summarize_re['top_n_summary'][0])
        i += 1
    # while (i < 10):
    #     print(data[i][0])
    #     summarize_re = summarize(data[i][0])
    #     summarizes_weekly.append(summarize_re['top_n_summary'][0])
    #     # print(summarize_re['top_n_summary'][0])
    #     i+=1
    # print("Database version : %s " % data)
    for s in summarizes_weekly:
        print(s)

    cursor.execute(var2, param1)
    data = cursor.fetchall()
    summarizes_monthly = []
    i = 0
    for d in data:
        print(d[0])
        summarize_re = summarize(d[0])
        summarizes_monthly.append(summarize_re['top_n_summary'][0])
        i += 1
    # while (i < 10):
    #     print(data[i][0])
    #     summarize_re = summarize(data[i][0])
    #     summarizes_monthly.append(summarize_re['top_n_summary'][0])
    #     # print(summarize_re['top_n_summary'][0])
    #     i+=1


    cursor.execute(var3, param2)
    data = cursor.fetchall()
    summarizes_daily = []
    i = 0
    for d in data:
        print(d[0])
        summarize_re = summarize(d[0])
        summarizes_daily.append(summarize_re['top_n_summary'][0])
        i += 1

    # while (i < 10):
    #     print(data[i][0])
    #     summarize_re = summarize(data[i][0])
    #     summarizes_daily.append(summarize_re['top_n_summary'][0])
    #     # print(summarize_re['top_n_summary'][0])
    #     i += 1

    summarizes = []
    summarizes.append(summarizes_weekly)
    summarizes.append(summarizes_monthly)
    summarizes.append(summarizes_daily)
    # 关闭数据库连接
    db.close()

    return summarizes

    # dict=summarize(u'腾讯科技讯（刘亚澜）10月22日消息，'
    #     u'前优酷土豆技术副总裁黄冬已于日前正式加盟芒果TV，出任CTO一职。'
    #     u'资料显示，黄冬历任土豆网技术副总裁、优酷土豆集团产品技术副总裁等职务，'
    #     u'曾主持设计、运营过优酷土豆多个大型高容量产品和系统。'
    #     u'此番加入芒果TV或与芒果TV计划自主研发智能硬件OS有关。'
    #     u'今年3月，芒果TV对外公布其全平台日均独立用户突破3000万，日均VV突破1亿，'
    #     u'但挥之不去的是业内对其技术能力能否匹配发展速度的质疑，'
    #     u'亟须招揽技术人才提升整体技术能力。'
    #     u'芒果TV是国内互联网电视七大牌照方之一，之前采取的是“封闭模式”与硬件厂商预装合作，'
    #     u'而现在是“开放下载”+“厂商预装”。'
    #     u'黄冬在加盟土豆网之前曾是国内FreeBSD（开源OS）社区发起者之一，'
    #     u'是研究并使用开源OS的技术专家，离开优酷土豆集团后其加盟果壳电子，'
    #     u'涉足智能硬件行业，将开源OS与硬件结合，创办魔豆智能路由器。'
    #     u'未来黄冬可能会整合其在开源OS、智能硬件上的经验，结合芒果的牌照及资源优势，'
    #     u'在智能硬件或OS领域发力。'
    #     u'公开信息显示，芒果TV在今年6月对外宣布完成A轮5亿人民币融资，估值70亿。'
    #     u'据芒果TV控股方芒果传媒的消息人士透露，芒果TV即将启动B轮融资。')

    # dict = summarize('随着邮轮上不断发现新型冠状病毒确诊病例，为了防止邮轮疫情暴发成为新冠病毒的“移动传染源”，代表全球60家成员的国际邮轮协会（CLIA）发布最严格的禁令，拒绝所有中国大陆出发的乘客和船员登船。这也意味着邮轮公司短期内已经基本撤出中国市场，中国邮轮市场进入了“冰封期”。2月3日，国际邮轮协会（CLIA）发布声明，暂停从中国大陆出发的船员往来，禁止过去14天内从中国大陆出发或者途径中国大陆的任何个人登船，包括乘客和船员。国际邮轮协会是世界上最大的邮轮行业协会，致力于邮轮行业的促进与发展。国际邮轮协会代表着60家成员，包括世界最大、最知名的邮轮公司，例如地中海邮轮、歌诗达邮轮、皇家加勒比邮轮、嘉年华邮轮、途易集团、阿依达邮轮等，占有全球近85%的市场份额，几乎涵盖了全球重要的中大型邮轮航线。国际邮轮协会在声明中称：”乘客的安全和健康是协会成员的第一要务。国际邮轮协会及其成员组织与世界卫生组织等世界各地的卫生专业人员和监管机构保持着密切联系，随着事态的发展不断评估和修改政策程序。这包括根据不断变化的情况在必要时修改行程，并根据全球卫生主管部门的现行指导，对近期来自或途径受影响地区的乘客及船员进行适当的筛查。依据具体情况做出明智决定，是否允许乘客或船员上船。“声明说：”重要的是，在管理和监控乘客及船员健康状况方面，邮轮行业是装备最完善、经验最丰富的行业之一。每艘均配备医疗设施，且“全天候”有医疗专业人员候命，可以应对突发卫生事件。邮轮公司会根据情况采取预防措施，在登船前对乘客和船员进行被动和主动筛查。此外，协会成员还采取了防疫措施和应对措施，所有船舶必须配备全天候24/7的医疗设施、船上和岸边医疗专业人员，以便提供初始医疗服务并防止疾病传播。“随着新型冠状病毒疫情进入爆发期，近期多名搭乘邮轮出游的中国乘客被确诊为新型冠状病毒肺炎。星梦邮轮”世界梦“号在1月29日从广州南沙出发前往越南的航程中有1名广东籍乘客确诊，船上有4428名乘客；后续1月24日从南沙出发前往香港的航程还搭载了607名乘客，共有5089名乘客接受了防控检查。公主邮轮”钻石公主“号在1月20日从日本横滨出发的航程中也有1名香港乘客确诊，船上共有2666名乘客，以及1045名船员。2月3日，这艘邮轮在重返横滨港之后，船上所有乘客和船员都接受了日本政府的检查，在抵达横滨前已有部分乘客出现发热等不适症状。歌诗达邮轮“Costa Smeralda”号在1月30日晚停')
    #dict = summarize('因海而生，向海而兴。1月12日上午10时，青岛航海文化研究会成立大会暨第一届会员大会召开。青岛航海文化研究会会员代表120多人参加会议。青岛是“一带一路”新欧亚大陆桥经济走廊的主要节点城市和海上合作支点的“双定位”城市，是建设海上丝绸之路的桥头堡，是国际合作的新平台。青岛拥有丰富的航海文化遗产和雄厚的航海文化资源。青岛航海文化研究会依托中国海洋大学、青岛大学、青岛科技大学、青岛社会科学院、青岛市社科联、青岛市文联、中科院海洋研究所、国家深海基地等教育科研文化单位，团结多年来从事航海科研、航海文化、航海运动、航运事业及旅游、海洋文化研究、对外交流合作方面的专家、科研工作者、管理人员，以传承航海文化成果，弘扬航海文化精神、促进航海事业发展为方向，深入挖掘青岛的航海文化资源，加强与海上丝绸之路沿线国家及长江以北、胶东半岛区域性合作，广泛开展航海文化理论和对策研究，促进航海、航运、航旅的文化学术交流及合作，助力青岛新旧动能转换“海洋攻势”，推动海洋经济高质量发展，打造国际海洋名城。青岛航海文化研究会将聚焦航海文化平台建设，聚沙成塔、握指成拳，通过组建航海历史文化研究、国际航海文化交流、航海文化作品创作、青少年航海及航海运动普及、旅游+航海等各专门工作委员会，跨界联合，多业融合，在科研、文化、旅游、体育等多个领域深度合作，共同推动航海文化事业的发展，不断提升和扩大青岛国际海洋文化名城的地位和影响，在海洋强国、海洋强省建设中出一份应尽的力量。会议审议通过了青岛航海文化研究会筹备工作报告、《章程》草案、选举办法，表决会费标准和管理办法，并选举产生了第一届理事会及常务理事会。山东省作家协会原副主席、国家一级作家、《第四极》《一个男人的海洋》等海洋作品的作者许晨先生当选为会长，田丰、曲金良、邹志、杨立敏、邵明磊、葛振营等七人当选为副会长，万蕾当选为秘书长。中国历史上第一位完成环球航海青岛籍女性水手宋坤当选为副会长。大会聘请中国环球航海第一人翟墨先生为特邀顾问。')
    # print('-----------approach 1-------------')


    # print(dict['top_n_summary'][0])
    # for sent in dict['top_n_summary']:
    #     print(sent)
    #
    # print('-----------approach 2-------------')
    # for sent in dict['mean_scored_summary']:
    #     print(sent)
    # abouttime()