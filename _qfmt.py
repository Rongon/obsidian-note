# -*- coding: utf-8 -*-
import pathlib, re

p = pathlib.Path(r"D:\FrontEnd\GitMd\WorkExperience.md")
s = p.read_bytes().decode("utf-8")

HEAD = "**面试官可能问的 5 个问题**"
NEW_HEAD = "### 四、面试官可能问的 5 个问题"

# 先抓出四节现有的 20 组问答（原格式：1. 问题 / 空行 /    **答**：答案）
pat = re.compile(r"^\d\. (?P<q>.+?)\n\n   \*\*答\*\*：(?P<a>.+?)(?=\n\n\d\. |\n\n---\n)", re.S | re.M)

def to_block(pairs):
    out = [NEW_HEAD, ""]
    for q, a in pairs:
        out.append("**Q：「%s」**" % q)
        out.append("A：「%s」" % a)
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"

for sec in ["2.1", "2.2", "2.3", "2.5"]:
    h = s.index("### " + sec)
    start = s.index(HEAD, h)
    end = s.index("\n---\n", start)
    chunk = s[start:end]
    pairs = [(m.group("q"), m.group("a")) for m in pat.finditer(chunk)]
    assert len(pairs) == 5, (sec, len(pairs))
    s = s[:start] + to_block(pairs) + "\n" + s[end + 1:]

p.write_bytes(s.encode("utf-8"))
print("ok")
