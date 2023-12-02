# Introduction
💬 Paper Intelligence Assistant is a PDF paper reading assistant based on large models, which can help users quickly read papers, extract viewpoints, summarize abstracts, and more.


# Background
Langchain is a very popular framework for developing large model applications, which can help us quickly develop lower level applications based on large models.

For those who are not familiar with the framework or only want to quickly develop certain individual applications, the learning cost will be relatively high.

Therefore, this article does not intend to use Langchain for development ❌， Instead, a small amount of code is used to implement the function of a paper reading assistant😄.


# Project Info
💡This project consists of two main modules, document extraction and a large base model.

## Paper extraction
For PDF format papers, the general format is a dual column layout. When processing these documents, we need to solve the following difficulties:
* Mixed Chinese and English: Domestic journal articles generally use Chinese as the main language, but certain paragraphs such as abstracts may be accompanied by English discussions
* Chaotic row and column layout: The paper is not simply strictly arranged according to rows or columns, but mixed together.
* Diverse formats: In addition to text, the paper also includes charts, formulas, etc., which often affects the accuracy of text extraction.

In summary, this project utilized the *pdfplumber* library and developed a document extraction strategy based on actual development experience.

## Base large model
⚠️This project was developed using Alibaba Cloud's DSW platform, so the images used in the models are all provided by the Magic Tower community (modelscope). If the user calls the model using other frameworks, such as Huggingface 🤭， You need to modify the framework and model ID yourself.
Considering the reading scenario of the paper, the required context may be relatively long, so Chatglm3-6b-32k dialogue model was used for development here. The usage method can be found in the official website [HF](https://huggingface.co/THUDM/chatglm3-6b-32k) or [Github](https://github.com/THUDM/ChatGLM3). 

# Usage
Enter*src*，run*assistant.py*(*file_path* Need to be modified according to actual situation)

```shell
cd src
python assistant.py
```
# Effect
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

