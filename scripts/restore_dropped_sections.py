import json,pathlib,re,sys
SP="/tmp/claude-1000/-home-camoa-workspace-dev-guides/3be71747-6c94-4508-86ec-1f774e96d0ab/scratchpad"
MAP=json.loads(pathlib.Path(f"{SP}/topic_source_map.json").read_text())
ROWS=json.loads(pathlib.Path(f"{SP}/dropped_verified.json").read_text())
args=[a for a in sys.argv[1:] if not a.startswith("--")]
only=args[0] if args else None
apply="--apply" in sys.argv

def partition_body(topic,slug):
    t=pathlib.Path(MAP[topic]).read_text()
    m=re.search(r'<!--\s*PARTITION:\s*%s\s*-->(.*?)<!--\s*END PARTITION'%re.escape(slug),t,re.S)
    return m.group(1) if m else None

def demote(md, from_lvl):
    """Source child level -> published '##'. Shift every heading by the same delta.

    Fenced code is masked first: a shell/YAML comment such as `# mymodule.services.yml`
    inside a fence is not a heading, and demoting it would invent one.
    """
    delta = 2 - from_lvl
    fences=[]
    def stash(m):
        fences.append(m.group(0)); return "\x00FENCE%d\x00"%(len(fences)-1)
    md = re.sub(r'```.*?```', stash, md, flags=re.S)
    def f(m):
        lvl=len(m.group(1))+delta
        return "#"*max(2,min(6,lvl))+" "+m.group(2)
    md = re.sub(r'^(#{1,6})\s+(.+)$', f, md, flags=re.M)
    for i,fb in enumerate(fences):
        md = md.replace("\x00FENCE%d\x00"%i, fb)
    return md

changed=0; added=0
for r in ROWS:
    key=f"{r['topic']}/{r['slug']}"
    if only and key!=only: continue
    body=partition_body(r["topic"],r["slug"])
    if body is None: continue
    heads=[(len(m.group(1)),m.group(2).strip()) for m in re.finditer(r'^(#{2,4})\s+(.+)$',body,re.M)]
    child=min(h[0] for h in heads)+1
    pat=re.compile(r'^(%s)\s+(.+?)$\n(.*?)(?=^#{2,%d}\s|\Z)'%('#'*child,child),re.M|re.S)
    secs=[(h,b) for _,h,b in pat.findall(body)]
    order=[h for h,_ in secs]
    want={g["heading"] for g in r["gone"]}
    p=pathlib.Path(r["published"]); ptxt=p.read_text()
    out=ptxt
    for idx,(h,b) in enumerate(secs):
        if h not in want: continue
        block = f"\n## {h.strip()}\n\n" + demote(b.strip(), child+1).strip() + "\n"
        # position: after the nearest PRECEDING sibling that exists in the page
        anchor=None
        for prev in reversed(order[:idx]):
            m=re.search(r'^##\s+%s\s*$'%re.escape(prev.strip()),out,re.M)
            if m: anchor=m; break
        if anchor:
            nxt=re.search(r'^##\s',out[anchor.end():],re.M)
            pos = anchor.end()+nxt.start() if nxt else len(out)
        else:
            m=re.search(r'^##\s+Common Mistakes\s*$',out,re.M) or re.search(r'^##\s+See Also\s*$',out,re.M)
            pos = m.start() if m else len(out)
        out = out[:pos].rstrip("\n") + "\n" + block + "\n" + out[pos:].lstrip("\n")
        added+=1
    if out!=ptxt:
        changed+=1
        if apply: p.write_text(out)
        else: print(f"WOULD PATCH {p}  (+{len([g for g in r['gone']])} sections)")
print(f"{'patched' if apply else 'would patch'}: {changed} files, {added} sections")
