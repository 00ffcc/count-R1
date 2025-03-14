
<h1 align="center">Count-R1</h1>

<div align="center">
    在数数任务上复现Deepseek-R1 ZERO
</div>

## task

没错，就是数数，从01串中数出0/1的个数。对于LLM来说，这个问题并没有你听起来这么简单。非reasoning模型完全不能解决这个问题(正确率与随机一样)，SOTA的reasoning模型(R1,o3-mini,claude3.7 thinking)也可以被轻易地构造数据hack掉。![image](https://github.com/user-attachments/assets/833202a5-a4de-46bf-9f92-b2333cd6b030)

## result

我在Qwen2.5 3B上成功复现了R1-zero(不使用冷启动)，观察到随着step的增加，response length和正确率不断同步增加。比较可惜的是没有观察到aha moment。
![image](https://github.com/user-attachments/assets/cc4ead0c-18eb-4c23-85c1-5f1264938c3e)

我还在Qwen2.5 3B和1.5B上使用不同的冷启动数据进行了实验。
![image](https://github.com/user-attachments/assets/e361825c-8125-4eaf-a29e-0047838d350a)


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

