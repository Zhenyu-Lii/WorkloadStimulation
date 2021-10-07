# 工作进度

## 2021.9.30 - 2021.10.7

### 工作简述 
使用Sequence Embedding来将用户行为转化为向量，目前使用了Sequence Graph Transform (SGT)
模型（Sequence Graph Transform (SGT): A Feature Embedding Function for Sequence Data Mining）

目前采用的方法是将用户的行为表示为一个sequence，它由0-5共6中行为组成，然后使用seq2vec方法将其转化为向量，最后进行聚类。

在工作过程中发现目前的session重复率很高，尝试截取了前1000条session，它们的用户行为都是一样的。
### 修改代码
新增SequenceEmbeddingService类，重新实现了represent方法，并与原论文中
提出的方法进行比对，结果有微小差异。

### TODO
继续寻找一些较新的Sequence Embedding相关方法的论文/代码，并尝试
用它们达到seq2vec的目的，并尝试阅读一下其实现代码。


