 #URL/Keyを書くとクラウドで問題を解くことができます。
 #ここではローカル実行を想定しているのでNoneとします。
url=None
key=None

 #Preparation of data
 #ノード1は15, ノード2は20だけ物資を有する
capacities = {1:15, 2:20} 
 #ノード3は7, ノード4は10, ノード5は15の要求がある
demands = {3:7, 4:10, 5:15}
 #このときアークにおけるコストは (1,3)=2, (1,5)=4, (2,4)=5, (2,5)=3なので
costs = {(1,3):2, (1,5):4, (2,4):5, (2,5):3}
source = range(1,3) #pythonでは range(i,j)は i...j-1まで
target  = range(3,6)

 #description of a problem
 #docplexをインポートする
from docplex.mp.model import Model
tm = Model(name='transportation')

 #decision (continuous) variable 
 #変数x(i,j)を問題tmの中に定義する．xは連続変数でiはsource，jはtargetを参照する．ただしこれはcostsに存在する (アークが繋がっている者同士) 場合に限る．
x = {(i,j): tm.continuous_var(name='x_{0}_{1}'.format(i,j)) for i in source for j in target if (i,j) in costs}
tm.print_information()

 #add constraints
 # (1,3), (1,5) を運ぶ物資の総量がcapacities[1]  (=15)を超えない
 # (2,4), (2,5) を運ぶ物資の総量がcapacities[2]  (=20)を超えない
for i in source:
    tm.add_constraint(tm.sum(x[i,j] for j in target if (i,j) in costs) <= capacities[i] )
for j in target:
    tm.add_constraint(tm.sum(x[i,j] for i in source if (i,j) in costs) >= demands[j] )

 #Objective function
 #目的関数はアーク(i,j)間に係る輸送コストの総量の最小化
tm.minimize(tm.sum(x[i,j]*costs[i,j] for i in source for j in target if (i,j) in costs))

 #Solve
 #問題を解く
tms = tm.solve(url=url,key=key)

 #Display and exceptions
 #解を表示
assert tms
tms.display()