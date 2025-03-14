<h1 align="center">Count-R1</h1>

<div align="center">
    在数数任务上复现Deepseek-R1 ZERO
</div>

## task

没错，就是数数，从01串中数出0/1的个数。对于LLM来说，这个问题并没有你听起来这么简单。非reasoning模型完全不能解决这个问题(正确率与随机一样)，SOTA的reasoning模型(R1,o3-mini,claude3.7 thinking)也可以被轻易地构造数据hack掉。(见下图。hint: 答案是20)

![](https://github.com/00ffcc/count-R1/blob/main/pics/QQ20250314-170413.jpg)

## result

我在Qwen2.5 3B上成功复现了R1-zero(不使用冷启动)，观察到随着step的增加，response length和正确率不断同步增加。比较可惜的是没有观察到aha moment。

![](https://github.com/00ffcc/count-R1/blob/main/pics/QQ20250314-170514.jpg)

我还在Qwen2.5 3B和1.5B上使用不同的冷启动数据进行了实验。

|模型|冷启动数据|结果|
|---|---|---|
|1.5B|不使用|失败，模型学到了format, 但是没有学习出CoT。|
|1.5B|从Deepseek v3蒸馏的CoT数据，不包含反思。|失败，模型从冷启动学到了format和CoT，正确率0.6, 但是RL中正确率没有提升，并且没有学习出反思。|
|1.5B|从Deepseek R1蒸馏的CoT数据，包含反思。|失败，模型在冷启动后出现了复读的情况，由于容易超出长度限制，format正确率和答案正确率都更低。|
|3B|不使用|成功，学习出了CoT，但是没有学习出反思。但是正确率为0.4, 不如直接蒸馏。|
|3B|从Deepseek R1蒸馏的CoT数据，包含反思。|失败，模型在冷启动后出现了复读的情况，由于容易超出长度限制，format正确率和答案正确率都更低。|

## conclusion
结论与R1报告一致：RL需要base model本身的能力作为种子。对于小模型，蒸馏从效率和效果来说都更优。

---

## Installation

```bash
conda create -n count python=3.9
pip3 install vllm==0.6.3 ray
pip3 install flash-attn --no-build-isolation
pip install -e .  # For verl integration
pip install wandb IPython matplotlib
```

---

## Training Execution
```bash
conda activate count
bash main_grpo.sh  # 6x3090
```

---

## ⚙️ Implementation Details

| Component              | Location                          |
|------------------------|-----------------------------------|
| Reward Modeling        | `verl/utils/reward_score/count.py`   |
| Data Preprocessing     | `examples/data_preprocess/count.py`  |
| Data distrill          | `sft/distrill.py`  |


---

## Acknowledgements
- [Verl](https://github.com/volcengine/verl) 🔗
- [Logic-RL](https://github.com/Unakar/Logic-RL) 🔗
- 感谢LDS实验室的算力支持，感谢吴俊康学长、黄科鑫学长的指导

