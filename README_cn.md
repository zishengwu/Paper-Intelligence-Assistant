# 项目介绍
💬 Paper Intelligence Assistant是一个基于大模型的PDF论文阅读助手，可以帮助用户快速进行论文阅读、观点提取、摘要总结等。


# 背景
langchain是一个非常热门的大模型应用开发框架，可以帮助我们快速开发基于大模型的下层应用。
对于不了解该框架或者只想要快速开发某些单独的应用而言，学习成本会比较高。
因此本文不打算使用langchain开发❌，而是用少量代码实现论文阅读助手这个功能。😄


# 功能介绍
💡本项目包含两个主要的模块，文档提取和底座大模型。

## 文档提取
对于PDF格式的论文，一般的格式都是双列布局，在处理这些文档时，我们需要解决以下难点：
* 中英文混杂：国内的期刊论文一般以中文为主，但是某些段落如摘要这些可能会附加英文论述
* 行列布局混乱：论文不是单纯严格按照行或者列布局，而是混合在一起。
* 格式多样：除了文字，论文中还包含图表，公式等，这往往会影响到文字提取的准确性。

综上所述，本项目用到了*pdfplumber*这个库，结合实际开发经验制定了文档提取策略。

## 底座大模型
⚠️本项目使用了阿里云的DSW平台进行开发，因此模型使用的镜像都是魔塔社区提供的（modelscope）。如果用户使用其他框架调用模型，如Huggingface🤭，需要自己修改框架和模型ID。
鉴于论文阅读场景，需要的上下文会比较长，因此这里使用了Chatglm3-6b-32k的对话模型进行开发，使用方式可以查看官方的
[HF](https://huggingface.co/THUDM/chatglm3-6b-32k) 或者 [Github](https://github.com/THUDM/ChatGLM3) 

# 使用方法
进入*src*目录，执行 *assistant.py* 即可(file_path需要根据实际情况修改)

```shell
cd src
python assistant.py
```
# 效果
```
**************************
欢迎使用论文阅读助手～
1.输入论文名称(仅支持pdf后缀文件)
2.输入您的问题
3.按`q`退出
**************************

玉米收储政策改革及其效应分析.pdf
论文解析成功！输入问题进行提问～

**************************
欢迎使用论文阅读助手～
1.输入论文名称(仅支持pdf后缀文件)
2.输入您的问题
3.按`q`退出
**************************

介绍这篇文章
这篇文章主要分析了2008年末出台的玉米临时收储政策在实现粮食增产、农民增收目标的同时，也产生了多方面负面影响。2016年取消临储政策后，玉米市场化改革开始启动，文章分析了这一改革对农民、市场和企业的影响。主要观点有：

1. 玉米临时收储政策调整后，农民收入出现下降，部分农民选择减少或缩减玉米种植面积。玉米价格下跌对农民形成强烈信号。 

2. 农民仍面临卖粮难的风险。国有粮食收储企业成为主要收购主体，但存在市场惯性，农民卖粮效率低。

3. 畜产品市场存在供给过剩风险，可能导致玉米市场波动。

4. 玉米市场化改革方案需要完善，如公布目标价格、创新农民增收思路、优化市场结构、建立预警机制等。

5. 玉米价格下跌为玉米加工业提供转型升级机会，应鼓励企业产品深度开发。

总体来说，文章系统分析了玉米临时收储政策改革的影响，提出了完善市场化改革、创新农民增收思路等政策建议。

```

