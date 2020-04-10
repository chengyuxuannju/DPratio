# 教程

## 环境配置

python2
rdseed
SAC

## 文件组织结构

* AXCC1

    * download/存放下载的文件

    * raw/ 存放分割后的文件，在此地进行SAC预处理
    
        * SAC_PZs_OO_AXCC1_BHZ(HDH) 仪器响应文件
    
    * rayleigh/ `cut_daily.py` 运行后会在这里生成供计算的数据
    
    * days DP_`daily.py` 运行生成的文本文件，记录的是计算出D/P ratio的日期
    
    * ratio `DP_daily.py` 运行生成的二进制文件，存储的是一个二维数据，假设为m*n，则m的大小和days的行数一致，n是ratio的数据长度   

* cut_daily.py 将`AXCC1/raw/`下的文件切成40000s长的可计算的文件，存储至`AXCC1/rayleigh/` 

* DP_daily.py 利用`AXCC1/rayleigh/` 的数据计算，结果存储至`AXCC1/` 的 days 和 ratio

* plot.py 绘图的程序，根据需要自行编写，调用计算结果和`rayleigh_plot.py` 内的绘图方法进行绘图和展示

* rayleigh_plot.py 绘图方法库， **部分方法用不到**

* rayleigh_utils.py 计算工具库

* README.md 教程

* station_db.py 将台站参数手动输入，运行后会产生`station.pkl`

* station.pkl `station_db.py`产生的文件，供其他文件调用，存储着台站信息

* transfer.sh 脚本文件，将其复制进`AXCC1/raw/`运行，对数据进行预处理

* split.py 将下载的数据分割成以天为单位

## 工作流程

### 准备工作

运行`station_db.py` 这里已经输入好了台站的信息，运行一次即可产生`station.pkl`文件，以后就不用管了


### 下载数据

2016年开始的数据均可，可先尝试下载某一个月的数据，跑通程序

所用数据为连续时间数据，下载的数据长度会参差不齐，后面的程序会进行处理

下载的文件可能是seed格式或者是mseed格式，可用rdseed软件解压

### 预处理

复制`split.py` 至 `AXCC1/download/`,运行`split.py`，在`AXCC1/raw`文件夹下产生分割好的文件

复制`transfer.sh` 至 `AXCC1/raw/` 

在 `AXCC1/raw/`文件夹下执行以下命令

```shell script
sh transfer.sh 
```

### 裁剪

cut_daily.py 将BHZ和HDH两个分量裁剪成头尾对齐，至少18000s长的文件（论文中提到计算采用2000s的片段，每天的结果至少用9个片段，所以此过程可确保每天的数据至少存在18000s连续的片段）

### 计算

DP_daily.py 产生两个文件，`AXCC1/days` 和 `AXCC1/ratio`

### 绘图
plot.py 尝试画出某天的D/P ratio 图

![](http://chengimage.oss-cn-beijing.aliyuncs.com/rayleigh/template.png)

这个图是一个示例，如果一切正常，画出来的图大概是这个样子的