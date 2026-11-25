# -*- coding: utf-8 -*-
"""book-0003 ch2 乱序修复：无跨章引用，仅内部 tag 重排"""
import re, glob, os

base = r'e:\2026\infinite-library\book-0003-世界模型导论\chapters'
f2 = [m for m in glob.glob(os.path.join(base, '*.md')) if re.match(r'02-', os.path.basename(m))][0]
t = open(f2, encoding='utf-8').read()

remap = {'4': '2', '5': '3', '2': '4', '6': '5', '3': '6'}
# 1,7,8,9,10,11,12 unchanged

print("修改前内联引用:", sorted(set(re.findall(r'式\s*\(?\s*2-(\d+)', t)), key=int))

for old, new in remap.items():
    t = t.replace('2-' + old, '2-TMP' + old)
for old, new in remap.items():
    t = t.replace('2-TMP' + old, '2-' + new)

open(f2, 'w', encoding='utf-8').write(t)

tags = re.findall(r'tag\{2-([0-9]+[a-z]?)\}', t)
nums = [int(x) for x in tags if x.isdigit()]
consec = nums == list(range(nums[0], nums[0] + len(nums)))
inlines_after = sorted(set(int(x) for x in re.findall(r'式\s*\(?\s*2-(\d+)', t)))
tagset = set(nums)
print("ch2 tags=%s consec=%s len=%d" % (tags, consec, len(t)))
print("内联引用:", inlines_after, "缺失:", set(inlines_after) - tagset)

# also verify no other chapter references 2-x
chdir = os.path.dirname(f2)
for m in glob.glob(os.path.join(chdir, '*.md')):
    k = int(re.match(r'(\d+)', os.path.basename(m)).group(1))
    if k == 2:
        continue
    tt = open(m, encoding='utf-8').read()
    for mm in re.finditer(r'式\s*\(?\s*2-(\d+)', tt):
        print("  CROSS-REF ch%d -> 式2-%s" % (k, mm.group(1)))
