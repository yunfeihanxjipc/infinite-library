import re, glob, os, sys, json

# Reverse-fix figure/table numbering that reorder.py clobbered.
# Only rewrites "图 N-x" and "表 N-x" (dash form) using the inverse map.
chdir = sys.argv[1]
ch = int(sys.argv[2])
inv = {int(k): int(v) for k, v in json.loads(sys.argv[3]).items()}  # new -> old

f = [m for m in glob.glob(os.path.join(chdir, '*.md'))
     if int(re.match(r'(\d+)', os.path.basename(m)).group(1)) == ch][0]
t = open(f, encoding='utf-8').read()

before_fig = re.findall(r'图\s*' + str(ch) + r'-(\d+)', t)
before_tab = re.findall(r'表\s*' + str(ch) + r'-(\d+)', t)
print('before 图:', before_fig, '表:', before_tab)

pat = re.compile(r'(图|表)\s*' + str(ch) + r'-(\d+)(?!\d)')

def sub(m):
    kind, num = m.group(1), int(m.group(2))
    return '%s %d-%d' % (kind, ch, inv.get(num, num))

t = pat.sub(sub, t)
open(f, 'w', encoding='utf-8').write(t)

after_fig = []
for x in re.findall(r'图\s*' + str(ch) + r'-(\d+)', t):
    x = int(x)
    if x not in after_fig:
        after_fig.append(x)
after_tab = []
for x in re.findall(r'表\s*' + str(ch) + r'-(\d+)', t):
    x = int(x)
    if x not in after_tab:
        after_tab.append(x)
print('after  图:', after_fig, '表:', after_tab)
