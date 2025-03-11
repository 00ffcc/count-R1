""" Preprocess dataset for knights and knaves logic task """

import os
import datasets
from tqdm import tqdm
import argparse
import json
import random


def make_prefix(s, t, template_type):

    if template_type == 'base':
        prefix = f"""The user asks a question, and the Assistant solves it.The assistant first thinks about the reasoning process in the mind and then provides the user with the final answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think><answer> answer here </answer>. Now the user asks you to solve a counting problem. After thinking, when you finally reach a conclusion, clearly state the answer within <answer> </answer> tags.\n\nUser: How many digits {t} are there in the string {s}?\nAssistant: <think> Let's think step by step, """
    elif template_type == 'qwen-instruct':
        prefix = f"""<|im_start|>system\nYou are a helpful assistant. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and<answer> </answer> tags, respectively, i.e., <think> reasoning process here </think><answer> answer here </answer>.  Now the user asks you to solve a counting problem. After thinking, when you finally reach a conclusion, clearly state the answer within <answer> </answer> tags.\n<|im_end|>\n<|im_start|>user\nHow many digits {t} are there in the string {s}?\n<|im_end|>\n<|im_start|>assistant\n<think> Let's think step by step, """
    return prefix

def gen_seq(num, max_length, vocab):
    res = []
    while len(res) < num:
        length = random.randint(5, max_length)
        r = (''.join(random.choices(vocab, k=length)), random.choice(vocab))
        if r not in res:
            res.append(r)
    return res


def gen_gen(seq, split):
    def gen():
        for idx, (s, t) in enumerate(seq):
            # 计算t在s中出现的次数
            ans = s.count(t)
            prompt = make_prefix(s, t, 'qwen-instruct')
            print(prompt)
            data = {
                    "data_source": "count",
                    "prompt": [{
                        "role": "user",
                        "content": prompt,
                    }],
                    "ability": "fact-reasoning",
                    "reward_model": {
                        "style": "rule",
                        "ground_truth": {
                            "target": ans,
                        }
                    },
                    "extra_info": {
                        'split': split,
                        'index': idx,
                    }
                }
            yield data
    return gen



if __name__ == '__main__':
    vocab = ['0', '1', '2']
    max_length=15
    train_num_words = 1024
    valid_num_words = 128

    all_words = gen_seq(train_num_words + valid_num_words, max_length=max_length, vocab=vocab)
    train_words = all_words[:train_num_words]
    valid_words = all_words[train_num_words:]

    # for i in gen_gen(train_words, 'train')():
    #     print(i)
    # exit()

    train_dataset = datasets.Dataset.from_generator(gen_gen(train_words, 'train'))
    valid_dataset = datasets.Dataset.from_generator(gen_gen(valid_words, 'valid'))

    # save as parquet
    train_dataset.to_parquet(f"../../data/counting_{len(vocab)}_{max_length}_train.parquet")
    valid_dataset.to_parquet(f"../../data/counting_{len(vocab)}_{max_length}_valid.parquet")