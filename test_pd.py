import pandas as pd

# 创建一个示例 DataFrame
data = {'A': [100, 200, 300,350], 'B': [2, 3, 1,0], 'C': [20, 10, 30,30]}
df = pd.DataFrame(data)

# 对 B 列进行排序
sorted_df = df.sort_values(by='B')
print(sorted_df)
if sorted_df['C'].is_monotonic_increasing:
    print('C 列为升序')
elif sorted_df['C'].is_monotonic_decreasing:
    print('C 列为降序')
else:
    print('C 列无序')