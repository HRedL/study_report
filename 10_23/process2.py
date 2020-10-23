import math
from covid_topic.result.topic_util2 import get_word_r_dict

word_path = f'rs_baidu.txt'
topic_path = f'topic2.txt'



def get_tokenized_doc(file_path):
    docs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for doc_str in f.readlines():
            doc = doc_str.strip('\n').split(',')
            if len(doc) != 0:
                docs.append(doc)
    return docs


def get_docs_words():
    """
    获取所有分号词的语料
    :return:
    """

    docs = get_tokenized_doc(word_path)
    return docs


def get_topic_words():
    """
    获取LDA提取的主题词的结果
    :return:
    """

    docs = get_tokenized_doc(topic_path)
    return docs


def getR(word_r_dict,word1, word2):

    """
    得到word1和word2的词共现关系
    :param word1:
    :param word2:
    :return:
    """
    return word_r_dict[word1,word2]


def getBG(word1, topic_num,topics,word_r_dict):
    """
    获取词word的BG
    :param word:
    :param topic_num:
    :return:
    """
    result = 0
    for i in range(len(topics)):
        if i != topic_num:
            first = math.log(get_edg(word1, topics[i]))
            second = 0
            for word2 in topics[i]:
                if word1 != word2:
                    second += getR(word_r_dict,word1, word2)
            result += first * second
    return result


def getTR(topic1, topic2):
    result = 0
    for word1 in topic1:

        edg = get_edg(word1,topic2)

        first = math.log(edg)
        second = 0
        for word2 in topic2:
            second += getR(word_r_dict,word1, word2)
        result += first * second

    return result


def get_edg(word1, topic):

    count = 1
    for word2 in topic:
        if hasR(word_r_dict,word1, word2):
            count += 1
    return count


def hasR(word_r_dict,word1, word2):
    if word_r_dict[word1,word2] != None:
        return True
    return False


def process_topic_tr(word_bgs_list,k):

    trs_list = []
    for i in range(len(word_bgs_list)):

        trs = []
        topic1 = word_bgs_list[i]
        for j in range(len(word_bgs_list)):
            if i != j:

                topic2 = word_bgs_list[j]

                tr = getTR(topic1, topic2)
                trs.append(tr)
            else:
                trs.append(0)

        trs_list.append(trs)

    results = []
    for i in range(len(trs_list)):
        for j in range(i):
            results.append((str(j) + "," + str(i), (float(trs_list[i][j]) + float(trs_list[j][i])) / 2))

    results = sorted(results, key=lambda x: x[1], reverse=True)

    merge_list = []

    for i in range(k):
        r = results[i][0].split(",")
        first = int(r[0])
        second = int(r[1])
        merge_list.append((first,second))


    word_merge_list = merge_topic(word_bgs_list,merge_list)

    word_m_list = []
    for word_merge in word_merge_list:
        if len(word_merge) != 0:
            word_m_list.append(word_merge)

    return word_m_list


def merge_topic(topics,merge_list):

    has_merged = {}
    for first,second in merge_list:
        if len(topics[first]) == 0:
            first = has_merged[first]
        topics[first].extend(topics[second])
        topics[first] = list(set(topics[first]))
        topics[second] = []
        has_merged[second] = first
    return topics



def process_topic_bg(topics,word_r_dict):
    """

    :return:
    """
    word_bgs_list = []

    for i in range(len(topics)):

        word_bgs = []
        for word in topics[i]:
            word_bg = getBG(word, i,topics,word_r_dict)
            word_bgs.append((word, word_bg))
            print(word, word_bg)
        word_bgs = sorted(word_bgs, key=lambda x: x[1], reverse=True)

        word_bgs_list.append(word_bgs)
    word_bgs_list = [[word_bg[0] for word_bg in word_bgs] for word_bgs in word_bgs_list]

    return word_bgs_list


def getKey(word1,topic,k):
    edg = get_edg(word1,topic)
    if edg < k:
        return 0
    first = math.log(edg)
    second = 0
    for word2 in topic:
        if word1 != word2:
            second += getR(word_r_dict,word1,word2)
    return first * second


def process_key(word_bgs_list,k):
    word_keys_list = []
    for word_bgs in word_bgs_list:
        word_keys = []
        for word_bg in word_bgs:
            word_key = getKey(word_bg, word_bgs, 4)
            word_keys.append((word_bg, word_key))
        word_keys = sorted(word_keys, key=lambda x: x[1], reverse=True)

        word_keys_list.append(word_keys)

    word_keys_list = [[word_key[0] for word_key in word_keys if word_key[1] != 0] for word_keys in word_keys_list]

    # for word_keys in word_keys_list:
    #     print(word_keys[:k])
    return [word_keys[:k]for word_keys in word_keys_list]


if __name__ == "__main__":
    K1 = 8
    K2 = 10
    K3 = 10
    topics = get_topic_words()
    docs = get_docs_words()
    word_r_dict = get_word_r_dict()


    #处理背景词
    word_bgs_list =  process_topic_bg(topics,word_r_dict)
    print("处理前:")
    for topic in word_bgs_list:
        print(topic)

    words = [word_bgs[K1:] for word_bgs in word_bgs_list ]
    print("去除背景词后:")
    for topic in words:
        print(topic)

    words = process_topic_tr(words,K2)
    print("相似子话题合并:")
    for topic in words:
        print(topic)

    words  = process_key(words,K3)
    print("提取关键词后:")
    for topic in words:
        print(topic)


