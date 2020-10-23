from gensim.corpora import Dictionary
import pandas as pd
import jieba
from gensim.models import  LsiModel
from covid_topic.prepare_data import get_tokenized_doc
from covid_topic.prepare_data import get_paths
import logging



def remove_words(docs):

    rm_words = []
    rm_words.append("疫情")

    docs = [[word for word in doc if word not in rm_words]for doc in docs]

    return docs





def save_model(docs,file_path):

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    dictionary = Dictionary(docs)

    # dictionary.filter_extremes(no_below=20, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    # model = TfidfModel(corpus)  # fit model
    # corpus = model[corpus]

    CHUNKSIZE = 500
    passes = 10
    temp = dictionary[0]


    NUM_TOPICS = 15
    model = LsiModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary)

    model.save(file_path)




if __name__ == "__main__":

    # file_path = f'data_fenci/all.txt'
    # docs = get_tokenized_doc(file_path)
    # save_model_path = "model/rm_words/all/lda_model.model"
    # save_model(docs, save_model_path)

    file_path = f'data_fenci/rs_baidu.txt'
    docs = get_tokenized_doc(file_path)
    save_model_path = "model/rm_words/baidu/lsa_model_15.model"
    save_model(docs,save_model_path)

    # file_path = f'data_fenci/rs_cn.txt'
    # docs = get_tokenized_doc(file_path)
    # save_model_path = "model/rm_words/cn/lda_model.model"
    # save_model(docs,save_model_path)
    #
    # file_path = f'data_fenci/rs_hit.txt'
    # docs = get_tokenized_doc(file_path)
    # save_model_path = "model/rm_words/hit/lda_model.model"
    # save_model(docs, save_model_path)
    #
    # file_path = f'data_fenci/rs_scu.txt'
    # docs = get_tokenized_doc(file_path)
    # save_model_path = "model/rm_words/scu/lda_model.model"
    # save_model(docs, save_model_path)