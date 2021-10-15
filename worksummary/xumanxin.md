# 工作进度
## 2021.9.30 - 2021.10.7
### 工作简述

#### 1.build_workload_intensity 加参数

在 build_workload_intensity 函数的实现中考虑了两个参数：

- interval_type（时间间隔类型，可为hour、minute等）
- t_interval（时间间隔大小）

目前两个参数必须在创建WESSBASIntensityService对象时就显式指定。

指定 interval_type 与 t_interval 后画出 intensity 趋势图的变化如下所示：第一张为加参数前结果，第二张为指定interval_type = 'hour'，t_interval = 1的结果

![intensity-before](https://tva1.sinaimg.cn/large/008i3skNly1gv7mgdjvmzj60hs0dc74p02.jpg)

![image-20211008034023976](https://tva1.sinaimg.cn/large/008i3skNly1gv7mgl2hdwj60hs0dcjry02.jpg)

#### 2.build_workload_intensity 返回值类型改变

build_workload_intensity() 函数的返回值类型从先前的大小为24*3600的 ndarray 转变为 dict<timespan，intensity>。

其中 timespan 为格式为 (start_time, end_time) 的 tuple，start_time、end_time 的类型都为 arrow.arrow.Arrow，一种类似于 datetime 的表示时间的类型。

timespan的大小，即$start\_time-end\_time$，由 interval_type 与 t_interval 共同决定。

#### 3.实现输入 timestamp 得到对应时间段内总 intensity

timestamp 的类型需为 arrow.arrow.Arrow，遍历build_workload_intensity() 的返回值找到落于的时间区间后得到 intensity。 

### TODO

- build_workload_intensity返回值的查找效率不理想，尤其是根据某一时间点找到某个时间段内的intensity，在数据量大的情况下可能需要进一步优化。

- 得到thinktime的正态分布，从而考虑一个session内存在多次请求。

## 2021.10.8 - 2021.10.14
### 工作简述
#### 1.阅读了Limbo有关论文，设想了通过参数模拟流量的可能方案
阅读了以下limbo论文：
- LIMBO: A Tool For Modeling Variable Load Intensities
Demo Paper
- Modeling Variations in Load Intensity over Time
- Modeling and Extracting Load Intensity Profiles

事实上这几篇文章的作者为同一个人
  
论文中提出了两大概念：
- DLIM：笛卡尔负载强度元模型（DLIM）提供了一种结构化和可访问的方式，通过编辑和组合数学函数来描述一段时间内的负载强度。
- HLDLIM：高层笛卡尔负载强度元模型（HLDLIM）允许使用少数参数来描述负载变化。

目前初步设想的解决方案步骤如下：
1. 根据原始日志文件生成原始时间序列
2. 从原始时间序列中分解出DLIM/HLDLIM特征
3. 调整DLIM/HLDLIM特征（对外暴露的API）
4. 合成新的原始时间序列

### TODO
1. 对于解决方案的可行性的进一步确认
2. 确定从时间序列中提取出DLIM还是HLDLIM
3. 代码复现解决方案