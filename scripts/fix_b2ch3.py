# -*- coding: utf-8 -*-
"""book-0002 ch3 乱序修复：ch15 三处跨章式引用内联化 + ch3 tag 重排连续"""
import re, glob, os

base = r'e:\2026\infinite-library\book-0002-自然语言智能导论\chapters'
f3 = [m for m in glob.glob(os.path.join(base, '*.md')) if re.match(r'03-', os.path.basename(m))][0]
f15 = [m for m in glob.glob(os.path.join(base, '*.md')) if re.match(r'15-', os.path.basename(m))][0]

# ===== 1) ch15：三处跨章引用内联化 =====
t = open(f15, encoding='utf-8').read()

old1 = "语言模型的核心挑战是第 3 章式 (3-1) 的链式分解带来的参数爆炸"
new1 = "语言模型的核心挑战是链式分解 $P(w_1,\\dots,w_T)=\\prod_{t=1}^{T}P(w_t\\mid w_1,\\dots,w_{t-1})$ 带来的参数爆炸"
assert old1 in t, "ch15 L33 未匹配"
t = t.replace(old1, new1)

old2 = "由链式法则（第 3 章式 3-1），整句概率分解"
new2 = "由链式法则，整句概率分解"
assert old2 in t, "ch15 L35 未匹配"
t = t.replace(old2, new2)

old3 = "第 3 章定义了困惑度（式 3-5）。"
new3 = "第 3 章定义了困惑度 $\\mathrm{PPL}(x)=\\exp\\!\\left(-\\frac{1}{T}\\sum_{t=1}^{T}\\log p_\\theta(w_t\\mid w_{<t})\\right)$。"
assert old3 in t, "ch15 L172 未匹配"
t = t.replace(old3, new3)

open(f15, 'w', encoding='utf-8').write(t)
print("ch15 三处引用已内联化")

# ===== 2) ch3：tag 重排（物理序 -> 连续） =====
remap = {'10': '2', '11': '3', '2': '4', '3': '5', '4': '6', '5': '7',
         '12': '8', '6': '9', '7': '10', '8': '11', '9': '12'}
# 1 和 13 不变
t = open(f3, encoding='utf-8').read()

# 先检查 ch3 内联引用分布
inlines = re.findall(r'式\s*\(?\s*3-(\d+)', t)
print("ch3 修改前内联引用:", inlines)

# 两阶段替换：先全部转占位符，再转新号（tag 和正文引用一起改）
for old, new in remap.items():
    t = t.replace('3-' + old, '3-TMP' + old)
for old, new in remap.items():
    t = t.replace('3-TMP' + old, '3-' + new)

open(f3, 'w', encoding='utf-8').write(t)

tags = re.findall(r'tag\{3-([0-9]+[a-z]?)\}', t)
nums = [int(x) for x in tags if x.isdigit()]
consec = nums == list(range(nums[0], nums[0] + len(nums)))
inlines_after = sorted(set(int(x) for x in re.findall(r'式\s*\(?\s*3-(\d+)', t)))
tagset = set(nums)
print("ch3 修改后 tags=%s consec=%s len=%d" % (tags, consec, len(t)))
print("ch3 内联引用(去重):", inlines_after, "缺失:", set(inlines_after) - tagset)
