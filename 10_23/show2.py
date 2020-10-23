from gensim.corpora import Dictionary
from gensim.models import LsiModel

from covid_topic.prepare_data import get_tokenized_doc
from covid_topic.prepare_data import get_paths


if __name__ =="__main__":
    # distribute_dcos()

    word_path = f'data_fenci/rs_baidu.txt'
    docs = get_tokenized_doc(word_path)
    paths = get_paths()

    dictionary = Dictionary(docs)

    corpus = [dictionary.doc2bow(doc) for doc in docs]


    # #8 主题
    # model = LdaModel.load("model/rm_words/baidu/lda_model_8.model")
    #
    # topic_list = model.show_topics()
    #
    # for topic in topic_list:
    #     print(topic)
    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())
    #
    # # 9 主题
    # model = LdaModel.load("model/rm_words/baidu/lda_model_9.model")
    #
    # topic_list = model.show_topics()
    #
    # for topic in topic_list:
    #     print(topic)
    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())
    #
    # #10主题
    # model = LdaModel.load("model/rm_words/baidu/lda_model_10.model")
    #
    # topic_list = model.show_topics()
    #
    # for topic in topic_list:
    #     print(topic)
    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())
    #
    # # 11主题
    # model = LdaModel.load("model/rm_words/baidu/lda_model_11.model")
    #
    # topic_list = model.show_topics()
    #
    # for topic in topic_list:
    #     print(topic)
    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())
    #
    # 12主题
    model = LsiModel.load("model/rm_words/baidu/lsa_model_15.model")

    topic_list = model.show_topics(num_topics=15,num_words=30)

    for topic in topic_list:
        print(topic)
    with open(f'result/topic2.txt', 'w', encoding='utf-8') as f:
        for i in range(15):
            words_ps = model.show_topic(i,topn=30)
            words_str = ""
            for word,p in words_ps:
                words_str += word +","
            words_str = words_str[:-1]
            f.write(words_str)
            f.write("\n")

    # words = model.show_topic(1, topn=30)
    # for word,p in words:
    #     print(word)

    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())
    #
    # # 13主题
    # model = LdaModel.load("model/rm_words/baidu/lda_model_13.model")
    #
    # topic_list = model.show_topics()
    #
    # for topic in topic_list:
    #     print(topic)
    # goodcm = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    # print(goodcm.get_coherence())