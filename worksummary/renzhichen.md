# 工作进度

## 2021.9.30 - 2021.10.7

### 工作简述 
使用Sequence Embedding来将用户行为转化为向量，目前使用了Sequence Graph Transform (SGT)
模型（Sequence Graph Transform (SGT): A Feature Embedding Function for Sequence Data Mining）
此方法也使用了一个6*6的矩阵来衡量一个行为对于另一个行为的影响，通过这种方法表示一个序列。与WESSBA原文中的方法不同的是，
此方法不仅考虑了相邻的行为之间的影响，也考虑了不相邻行为之间的影响，且距离越远影响越小，是一种更为全面的建模方法。
不过此方法仍然没有能够很好的利用序列中的顺序信息，因此还需要寻找新的模型。

在工作过程中发现目前的session重复率很高，尝试截取了前1000条session，它们的用户行为都是一样的。
### 修改代码
新增SequenceEmbeddingService类，重新实现了represent方法，并与原论文中
提出的方法进行比对，结果有微小差异。

### TODO
继续寻找一些较新的Sequence Embedding相关方法的论文/代码，并尝试
用它们达到seq2vec的目的，并尝试阅读一下其实现代码。

## 2021.10.8 - 2021.10.15

### 工作简述
本周的主要工作内容为寻找用户行为建模的相关方法。
阅读了《Perceive Your Users in Depth: Learning Universal User Representations from Multiple E-commerce Tasks》论文，
此论文提出了一个多任务训练模型，通过该模型，我们可以根据用户行为序列抽取出用户的特征， 且使用此模型得到的用户特征在多种下游任务中都有着良好的表现。
在这篇文章所提出的模型中，用户行为序列首先会经过LSTM与attention层进行特征的提取（这一步的结果也正是我们需要的），随后再进行下游任务的训练，
在这一过程中更新LSTM与attention中的权重。

但目前我们的工作中缺乏对应的下游任务，因此目前来说这一方法并不适用。但如果能够有对应的下游任务与数据的支持，我认为这个思路值得尝试。

此外，我在检索sequence embedding相关工作的时候检索到了较多蛋白质序列embedding的论文，如果不考虑用户行为序列与蛋白质序列的实际意义，这两个任务
具有一定的相似性，例如不同的长度可能具有相似的特征，我将在接下来的时间中阅读相关文献并研究文献中所提出的方法能否应用于我的任务中。

### TODO
从WESSBA论文与SGT论文的被引论文中寻找可行的用户行为建模方法。

尝试阅读论文《LEARNING PROTEIN SEQUENCE EMBEDDINGS USING INFORMATION FROM STRUCTURE》
，并判断文中处理基因序列的方法是否能够应用于用户行为序列的建模工作中。


