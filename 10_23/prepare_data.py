import pandas as pd
import os
import jieba
import random
import re
import jieba.posseg

def remove_stopword(docs,stopword_file):
    """
    去除停用词
    :param docs: [[],[]]
    :return: [[],[]]
    """
    #获取停用词表
    file = open(stopword_file, 'r+', encoding='utf-8')
    stopwords = file.read().split("\n")
    rs_docs =[]
    punc_str = '。|，|,|;|；|\.|\?'
    for doc in docs:
        rs_doc = []

        for word in doc:
            if len(re.findall(r'\W',word)) > 0:
                print("标点符号",word)
            elif len(re.findall(r'\d+', word))> 0:
                print("数字",word)
            elif word in stopwords:
                print("停用词",word)
            elif len(word) <= 1:
                print("单字符",word)
            elif word == "":
                print("空字符串",word)
            elif len(re.findall(r'[a-zA-Z]+',word)) > 0:
                print("英文",word)
            else:
                rs_doc.append(word)
        rs_docs.append(rs_doc)
    return rs_docs



def get_file_path(dir):
    files = os.listdir(dir)
    file_paths =[]
    for file in files:
        file_path = os.path.join(dir,file)
        file_paths.append(file_path)
    return file_paths



def get_docs():
    dir_m = "data_processed/mafengwo"
    dir_q = "data_processed/qiongyou"
    dir_x = "data_processed/xiecheng"
    file_paths = []
    docs = []
    file_paths.extend(get_file_path(dir_m))
    file_paths.extend(get_file_path(dir_q))
    file_paths.extend(get_file_path(dir_x))

    random.shuffle(file_paths)
    for file in file_paths:
        with open(file, 'r', encoding="utf-8") as f:
            doc = pd.read_csv(f, header=None).iloc[:,0].astype("str")
            docs.append(doc)

    return docs,file_paths


def tokenize_doc(doc):
    words =[]
    jieba.add_word("健康码")
    jieba.add_word("核酸检测")
    jieba.add_word("新冠")
    jieba.add_word("新型冠状病毒")
    jieba.add_word("绿码")

    for sentence in doc:
        words_seq =jieba.cut(sentence)
        words_seq = [x.strip() for x in words_seq if x.strip() != '']
        words_seq = [x if x != "," else "，" for x in words_seq]
        words.extend(words_seq)

    return words


def save_tokenized_doc(words_list,file_path=f'data_fenci/all.txt'):

    with open(file_path, 'w', encoding="utf-8") as f:
        for words in words_list:
            doc = ""
            for word in words:
                doc = doc + word +","
            doc = doc[:-1]
            if doc=="":
                continue
            f.write(doc)
            f.write("\n")


def get_tokenized_doc(file_path=f'data_fenci/all.txt'):
    docs = []
    with open(file_path,'r',encoding='utf-8') as f:
        for doc_str in f.readlines():
            doc = doc_str.strip('\n').split(',')
            if len(doc)!=0:
                docs.append(doc)
    return docs


def save_paths(paths,file_path = f'data_fenci/path.txt'):
    with open(file_path, 'w', encoding="utf-8") as f:
        for path in paths:
            f.write(path)
            f.write("\n")


def get_paths(file_path = f'data_fenci/path.txt'):

    with open(file_path, 'r', encoding="utf-8") as f:
        paths = f.readlines()
        paths = [path.strip('\n') for path in paths]

    return paths

def save_all_docs_and_paths():
    file_path = f'data_fenci/all.txt'
    docs,paths = get_docs()
    words_list = []
    for doc in docs:
        words =tokenize_doc(doc)
        words_list.append(words)
    save_tokenized_doc(words_list,file_path)
    save_paths(paths)

def save_rs_docs(stopword_file,rs_docs_file_path):
    all_docs_file_path = f'data_fenci/all.txt'
    if not os.path.exists(all_docs_file_path):
        save_all_docs_and_paths()

    docs = get_tokenized_doc()


    docs = remove_stopword(docs, stopword_file)


    save_tokenized_doc(docs, rs_docs_file_path)


if __name__ =="__main__":
    # save_all_docs_and_paths()
    # #scu
    # stopword_file = 'stopword/scu_stopwords.txt'
    # rs_docs_file_path = f'data_fenci/rs_scu.txt'
    # save_rs_docs(stopword_file,rs_docs_file_path)

    #baidu
    stopword_file = 'stopword/baidu_stopwords.txt'
    rs_docs_file_path = f'data_fenci/rs_baidu.txt'
    save_rs_docs(stopword_file, rs_docs_file_path)
    # #cn
    # stopword_file = 'stopword/cn_stopwords.txt'
    # rs_docs_file_path = f'data_fenci/rs_cn.txt'
    # save_rs_docs(stopword_file, rs_docs_file_path)
    # #hit
    # stopword_file = 'stopword/hit_stopwords.txt'
    # rs_docs_file_path = f'data_fenci/rs_hit.txt'
    # save_rs_docs(stopword_file, rs_docs_file_path)




