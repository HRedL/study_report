
import multiprocessing as mp
import pandas as pd
import numpy as np

def get_tokenized_doc(file_path=f'rs_baidu.txt'):
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
    word_path = f'rs_baidu.txt'
    docs = get_tokenized_doc(word_path)
    return docs


def get_topic_words():
    """
    获取LDA提取的主题词的结果
    :return:
    """
    word_path = f'topic.txt'
    docs = get_tokenized_doc(word_path)
    return docs


def getR(docs,word1, word2):

    """
    得到word1和word2的词共现关系
    :param word1:
    :param word2:
    :return:
    """
    if word1 == word2:
        return 1.0
    count1 = 0
    count2 = 0
    for doc in docs:
        if word2 in doc:
            count2 += 1/len(doc)
            if word1 in doc:
                count1 += 1 / len(doc)

    return  count1/count2


def getALLR():
    docs = get_docs_words()
    topics = get_topic_words()
    words = []
    for topic in topics:
        words.extend(topic)
    words = list(set(words))




    num_cpus = mp.cpu_count() #获取机器cpu的个数
    pool = mp.Pool(num_cpus)
    results =[]
    for word1 in words:
        result = pool.apply_async(process_r,args=(docs,word1,words))
        results.append(result)


    pool.close()
    pool.join()
    rs_list = []
    for result in results:
        word1,rs = result.get()
        rs_list.append((word1,rs))

    data_list = []
    for word1,rs in rs_list:
        for i in range(len(words)):
            data_list.append([word1,words[i],rs[i]])


    dataset = pd.DataFrame(data_list, columns=['word1','word2','r'])
    save_path = f'word_r.csv'
    # 处理换行、空格、数字
    dataset.to_csv(save_path, index=False, encoding='utf-8')



def get_word_r_dict():
    with open("word_r.csv", 'r', encoding='utf-8') as f:
        results = pd.read_csv(f)
        word_r_dict = {}
        for i in range(len(results)):

            word_r_dict[results.loc[i][0],results.loc[i][1]] = results.loc[i][2]

    return word_r_dict


def process_r(docs,word1,words):
    rs =[]
    for word2 in words:
        rs.append(str(getR(docs,word1,word2)))

    return word1,rs






if __name__ == "__main__":
    getALLR()
    # docs = get_docs_words()
    # topics = get_topic_words()
    # words = []
    # for topic in topics:
    #     words.extend(topic)
    # words = list(set(words))
    # getR2(docs,words,words)
