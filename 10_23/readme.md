# txt文件

### all.txt

分词后的数据

### rs_baidu.txt

去除停用词后的数据

### topic2.txt

LDA提取的结果

### 最终结果.txt

GPLSA处理后的最终结果

# python文件

### prepare_data.py

处理数据，可以在这修改分词的代码

### model.py

LDA

### model_lsi.py

LSA

### show2.py

查看LDA的结果，并将话题写入文件

### topic_util.py

计算所有词的共现关系（运行时间较长）

### process2.py

根据词共现关系进行1.去除背景词，2.相似子话题合并，3.提取关键词

# 论文

ELDA

面向社交媒体评论的子话题挖掘研究

process2.py是第二篇论文的实现，

第一篇论文的实现相当于将process2.py文件中的提取关键词和相似子话题合并这两个过程调换一下位置

