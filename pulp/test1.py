import pandas as pd
import numpy as np
import pulp

df = pd.read_csv("mac.csv",index_col=0)

# 欠損値を0埋め
df = df.fillna(0)

# カロリーが0の商品を除く
df = df[df['エネルギー kcal']>0]

# 栄養値の上限・下限の入力
df_max_min = pd.read_csv("balance.csv",index_col=0)

# 変数の設定
df["個数"] = pulp.LpVariable.dicts('個数',df.index,lowBound=0,upBound=3,cat='Integer').values()

# 最小化問題
problem = pulp.LpProblem('完全栄養マクドナルド問題',sense=pulp.LpMinimize)

# 目的変数の設定
problem.setObjective(pulp.lpDot(df["エネルギー kcal"],df["個数"]))

"""
if not np.isnan(df_max_min.loc["たんぱく質 g","上限"]):
    print("!")
else:
    print("?")
    problem.addConstraint(pulp.lpDot(df["たんぱく質 g"],df["個数"])>=df_max_min.loc["たんぱく質 g","上限"])

"""
for nutrition in df_max_min.index:
    if not np.isnan(df_max_min.loc[nutrition,"上限"]):
       print(nutrition,"の上限は",df_max_min.loc[nutrition,"上限"])
    if not np.isnan(df_max_min.loc[nutrition,"下限"]):
       print(nutrition,"の下限は",df_max_min.loc[nutrition,"下限"])


nutrition="たんぱく質 g"
if not np.isnan(df_max_min.loc[nutrition,"上限"]):
    problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])<=df_max_min.loc[nutrition,"上限"])
if not np.isnan(df_max_min.loc[nutrition,"下限"]):
    problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])>=df_max_min.loc[nutrition,"下限"])

nutrition="脂質 g"
if not np.isnan(df_max_min.loc[nutrition,"上限"]):
    problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])<=df_max_min.loc[nutrition,"上限"])
if not np.isnan(df_max_min.loc[nutrition,"下限"]):
    problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])>=df_max_min.loc[nutrition,"下限"])
"""
# 拘束条件
for nutrition in df_max_min.index:
    if not np.isnan(df_max_min.loc[nutrition,"上限"]):
      problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])<=df_max_min.loc[nutrition,"上限"])
    if not np.isnan(df_max_min.loc[nutrition,"下限"]):
      problem.addConstraint(pulp.lpDot(df[nutrition],df["個数"])>=df_max_min.loc[nutrition,"下限"])
      

# 重量に条件
problem.addConstraint(pulp.lpDot(df["製品重量"],df["個数"])<=2000)

# 問題を解く
status = problem.solve()
print(pulp.LpStatus[problem.status])

# 答えの表示
for v in problem.variables():
  if v.varValue != 0:
    print(f'{v.name} = {v.varValue}')

print(f"総カロリー:{pulp.value(problem.objective)}kcal")

for nutrition in df_max_min.index:
  print(nutrition + ":" + str(round(pulp.lpDot(df[nutrition], df["個数"]).value(),ndigits=1)))
"""