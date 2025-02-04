
# Logic R1 

## Successfully reproduced DeepSeek R1's zero-shot performance on 2K Logic Puzzle Dataset.
See project explanation [here](https://evxpwrsfkdb.feishu.cn/docx/NokEdaMBmo6aqZxVdxkcSm2cnab?from=from_copylink).

Wandb project page & Logs are coming soon.

---

## ✨ Enhanced Features (After Rule-Based RL)

| 🚩 Uncertainty Marking | 🔀 Multi-path Exploration |
|------------------------|---------------------------|
| Flagging ambiguous steps for verification | Testing alternative reasoning paths |

| 🔍 Analytical Backtracking | 📝 Progressive Summarization |
|---------------------------|-----------------------------|
| Re-examining previous statements through re-analysis | Maintaining intermediate conclusions via explicit summaries |

| ✅ Final-answer Verification | 🌐 Multilingual CSwitching |
|-----------------------------|-------------------------------|
| Comprehensive consistency checks before output | Chinese reasoning traces with English answers |

---

## 📸 Results Preview

<table>
  <tr>
    <td align="center"><img src="response.png" width="400" alt="Model Output"></td>
    <td align="center"><img src="mean_length.png" width="400" alt="Output Length"></td>
  </tr>
  <tr>
    <td align="center">Model Output Example</td>
    <td align="center">Average Output Length</td>
  </tr>
</table>

---

## 🛠️ Installation

```bash
conda create -n logic python=3.9
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121
pip3 install vllm==0.6.3 ray
pip3 install flash-attn --no-build-isolation
pip install -e .  # For verl integration
pip install wandb IPython matplotlib
```

---

## 📂 Data Preparation

### Base Model
```bash
python ./examples/data_preprocess/kk.py \
    --local_dir {processed_data_path} \
    --data_path {raw_data_path}
```

### Instruct-Tuned Model
```bash
python ./examples/data_preprocess/kk.py \
    --template_type=qwen-instruct \
    --local_dir {processed_data_path} \
    --data_path {raw_data_path}
```

---

## 🚀 Training Execution
```bash
conda activate logic
bash main_grpo.sh  # 4×A100 80G
```

---

## ⚙️ Implementation Details

| Component              | Location                          |
|------------------------|-----------------------------------|
| 🏆 Reward Modeling     | `verl/utils/reward_score/kk.py`   |
| ⚙️ Training Config    | `scripts/train_ppo.sh`            |
| 💻 Hardware Setup      | 4-GPU (modify in `kk.sh`)         |
| 📊 Monitoring          | Weights & Biases (requires login) |

---

## 🙏 Acknowledgements
[TinyZero](https://github.com/Jiayi-Pan/TinyZero) 🔗
