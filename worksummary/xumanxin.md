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

