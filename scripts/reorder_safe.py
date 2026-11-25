import re, glob, os, sys, json

# SAFE reorder: only renumbers formula tags \tag{N-M} and inline refs 式 N-M.
# Does NOT touch 图 N-M / 表 N-M / 例 N.M / 定义 N.M etc.
chdir = sys.argv[1]
ch = int(sys.argv[2])
mapping = {int(k): int(v) for k, v in json.loads(sys.argv[3]).items()}

f = [m for m in glob.glob(os.path.join(chdir, '*.md'))
     if int(re.match(r'(\d+)', os.path.basename(m)).group(1)) == ch][0]
t = open(f, encoding='utf-8').read()
before = re.findall(r'tag\{%d-([0-9]+[a-z]?)\}' % ch, t)
print('before tags:', before)

# 1) Fix \tag{N-M} occurrences
def sub_tag(m):
    old = int(m.group(1))
    return '\\tag{%d-%d}' % (ch, mapping.get(old, old))
t = re.sub(r'\\tag\{%d-(\d+)\}' % ch, sub_tag, t)

# 2) Fix inline formula refs: patterns like "式 N-M", "式(N-M)", "（式 N-M）"
# These have 式 before the number
def sub_ref(m):
    old = int(m.group(1))
    return m.group(0).replace('%d-%d' % (ch, old), '%d-%d' % (ch, mapping.get(old, old)))
# Match: 式 optional-space optional-( N-M optional-)
t = re.sub(r'(式\s*\(?[ ]*)%d-(\d+)(\)?[ ]*)' % ch, 
           lambda m: m.group(1) + '%d-%d' % (ch, mapping.get(int(m.group(2)), int(m.group(2)))) + m.group(3), t)

open(f, 'w', encoding='utf-8').write(t)
after = re.findall(r'tag\{%d-([0-9]+[a-z]?)\}' % ch, t)
nums = [int(x) for x in after if x.isdigit()]
print('after tags:', after, 'consec:', nums == list(range(1, len(nums) + 1)))
print('len:', len(t))
