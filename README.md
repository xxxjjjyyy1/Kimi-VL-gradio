# 1.基础配置
**服务器配置：GPU 两块RTX4090 ,内存至少65G**

**系统：Ubuntu22.04**

**模型：**

+ Kimi-VL-Instruct：对于一般的多模态感知和理解、OCR、长视频和长文档、视频感知和智能体使用，我们推荐 Kimi-VL-A3B-Instruct 进行高效推理
+ Kimi-VL-A3B-Thinking 对于高级文本和多模态推理（例如数学），请考虑使用 Kimi-VL-A3B-Thinking

**模型论文成果：**[Kimi-VL Technical Report](https://arxiv.org/abs/2504.07491)  

**项目开源地址:**  [Kimi-VL](https://github.com/MoonshotAI/Kimi-VL?tab=readme-ov-file)

**我使用的环境是：python=3.10,cuda=12.1**

# 2.界面展示
由于Kimi团队并没有给出开源的操作界面，我写了一个简单的gradio操作界面

![](https://cdn.nlark.com/yuque/0/2025/png/55420051/1744866199604-7157e12e-8499-46d7-a8e2-bf7091fbc1b9.png)

**效果展示：**

![](https://cdn.nlark.com/yuque/0/2025/png/55420051/1744866216142-b7fb8ee2-f7e1-4f5e-ae47-697b0b585b8f.png)

# 3.引用
```plain
@misc{kimiteam2025kimivltechnicalreport,
      title={{Kimi-VL} Technical Report}, 
      author={Kimi Team and Angang Du and Bohong Yin and Bowei Xing and Bowen Qu and Bowen Wang and Cheng Chen and Chenlin Zhang and Chenzhuang Du and Chu Wei and Congcong Wang and Dehao Zhang and Dikang Du and Dongliang Wang and Enming Yuan and Enzhe Lu and Fang Li and Flood Sung and Guangda Wei and Guokun Lai and Han Zhu and Hao Ding and Hao Hu and Hao Yang and Hao Zhang and Haoning Wu and Haotian Yao and Haoyu Lu and Heng Wang and Hongcheng Gao and Huabin Zheng and Jiaming Li and Jianlin Su and Jianzhou Wang and Jiaqi Deng and Jiezhong Qiu and Jin Xie and Jinhong Wang and Jingyuan Liu and Junjie Yan and Kun Ouyang and Liang Chen and Lin Sui and Longhui Yu and Mengfan Dong and Mengnan Dong and Nuo Xu and Pengyu Cheng and Qizheng Gu and Runjie Zhou and Shaowei Liu and Sihan Cao and Tao Yu and Tianhui Song and Tongtong Bai and Wei Song and Weiran He and Weixiao Huang and Weixin Xu and Xiaokun Yuan and Xingcheng Yao and Xingzhe Wu and Xinxing Zu and Xinyu Zhou and Xinyuan Wang and Y. Charles and Yan Zhong and Yang Li and Yangyang Hu and Yanru Chen and Yejie Wang and Yibo Liu and Yibo Miao and Yidao Qin and Yimin Chen and Yiping Bao and Yiqin Wang and Yongsheng Kang and Yuanxin Liu and Yulun Du and Yuxin Wu and Yuzhi Wang and Yuzi Yan and Zaida Zhou and Zhaowei Li and Zhejun Jiang and Zheng Zhang and Zhilin Yang and Zhiqi Huang and Zihao Huang and Zijia Zhao and Ziwei Chen},
      year={2025},
      eprint={2504.07491},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.07491}, 
}
```

<font style="color:rgb(51, 51, 51);">  
</font>





