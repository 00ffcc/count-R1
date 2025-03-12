import asyncio
import json
import random
import re
from openai import AsyncOpenAI

# Create async client
async_client = AsyncOpenAI(
    api_key="sk-vazbgordvzhtuctmsruykttigikzxyjvmdcaloeyxyztkmlm",
    base_url="https://api.siliconflow.cn/v1"
)

system_prompt = "You are a helpful assistant. The assistant first thinks about the reasoning process and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think><answer> answer here </answer>.  Now the user asks you to solve a logical reasoning problem. After thinking, when you finally reach a conclusion, clearly state the answer within <answer> </answer> tags."

def gen_seq(num, max_length, vocab):
    res = []
    while len(res) < num:
        length = random.randint(5, max_length)
        seq = ''.join(random.choices(vocab, k=length))
        t = random.choice(vocab)
        if (seq, t) not in res:
            res.append((seq, t))
    return res

async def process_sequence(seq, t):
    content = f"How many digits {t} are there in the string {seq}?"
    try:
        response = await async_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {"role": "user", "content": content+' Summarize your thinking in <summary> </summary>. After thinking, when you finally reach a conclusion, clearly state the answer within <answer> </answer> tags.'},
            ]
        )
        
        gt = seq.count(t)
        thinking = response.choices[0].message.reasoning_content
        res = response.choices[0].message.content
        print("thinking: ", thinking)
        print("answer: ", res)
        matches = list(re.finditer(r'<answer>(.*?)</answer>', res, re.DOTALL))
        
        try:
            summarized_thinking = list(re.finditer(r'<summary>(.*?)</summary>', res, re.DOTALL))[-1].group(1).strip()
            ans = int(matches[-1].group(1).strip())
            print(ans, gt, seq)
            
            if ans == gt:
                return {
                    "instruction": content,
                    "input": "",
                    "output": f"<think>\n{summarized_thinking}\n</think>\n<answer>\n{ans}\n</answer>",
                    "system": system_prompt,
                }
        except (IndexError, ValueError):
            print(f"Could not find valid answer in response for {seq}")
        
    except Exception as e:
        print(f"Error processing {seq}: {str(e)}")
    
    return None

async def main():
    max_length = 40
    # Generate sequences
    sequences = gen_seq(1, max_length, ['0', '1'])
    
    # Process sequences concurrently with a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent requests
    
    async def bounded_process(seq, t):
        async with semaphore:
            return await process_sequence(seq, t)
    
    tasks = [bounded_process(seq, t) for seq, t in sequences]
    results = await asyncio.gather(*tasks)
    
    # Filter out None results and save to file
    js = [result for result in results if result is not None]
    
    with open(f'count_sft_data_{max_length}.json', 'w') as f:
        json.dump(js, f)
    
    print(f"Successfully processed and saved {len(js)} valid examples")

if __name__ == "__main__":
    asyncio.run(main())