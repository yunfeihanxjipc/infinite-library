import re,sys
f=sys.argv[1]
c=open(f,encoding='utf-8').read()
print('chars',len(c))
tags=re.findall(r'\\tag\{(\d+-\d+)\}', c)
print('tags in doc order:', tags)
exs=re.findall(r'例 (\d+\.\d+[a-z]?)', c)
print('examples:', exs)
tabs=re.findall(r'表 (\d+-\d+)', c)
print('tables:', tabs)
defs=re.findall(r'定义 (\d+\.\d+)', c)
print('defs:', defs)
# check tag continuity: extract prefix and numbers
from collections import Counter
for grp in sorted(set(t.split('-')[0] for t in tags)):
    nums=[int(t.split('-')[1]) for t in tags if t.split('-')[0]==grp]
    seq=nums
    ok = seq==list(range(1,len(seq)+1))
    print(f'group {grp}: count={len(seq)} max={max(seq) if seq else 0} continuous_1..K={ok}')
