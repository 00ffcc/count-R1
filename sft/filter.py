import json

with open('count_sft_data_30.json') as f:
    data = json.load(f)

length = []
for i in data:
    length.append(len(i['output']))

# 画出length的频次分布
import matplotlib.pyplot as plt
plt.hist(length, bins=100, range=(0, 10000))
plt.xlabel('length')
plt.ylabel('frequency')
plt.title('length distribution')
plt.savefig('length_distribution.png')

new_data = []
for i in data:
    if len(i['output']) < 4000:
        new_data.append(i)

with open('count_sft_data_30_short.json', 'w') as f:
    json.dump(new_data, f)