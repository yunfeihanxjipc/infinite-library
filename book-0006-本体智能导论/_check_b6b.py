import re, os
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters')
files = [
 '25-可微逻辑与可微推理.md',
 '26-图神经网络与逻辑推理.md',
 '27-符号知识与深度学习的结合.md',
 '28-神经符号的评估与局限.md',
 '29-大语言模型中的知识.md',
 '30-检索增强与知识图谱增强.md',
 '31-幻觉与知识边界.md',
]
pat = re.compile(r'\\tag\{(\d+)-(\d+)\}')
for f in files:
    t = open(os.path.join(d, f), encoding='utf-8').read()
    n = len(t)
    tags = [b for a, b in pat.findall(t)]
    # check sequential 1..M
    ok = (tags == [str(i) for i in range(1, len(tags)+1)])
    # sub-examples order check: find 例 N.M and 例 N.Mb
    examples = re.findall(r'\*\*例 (\d+)\.(\d+)([a-z]?)\b', t)
    print(f'{n:6d}  ntag={len(tags):2d} seq_ok={ok}  {f[:10]}')
    print('        tags:', tags)
    print('        examples:', examples)
