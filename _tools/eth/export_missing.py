"""Write English text of recipes that lack Amharic or Oromo to the given output file.
Usage: python3 export_missing.py path/to/index.html out.txt [langs, default am,om,tl]"""
import sys,re,json
html,out=sys.argv[1],sys.argv[2]
LANGS=(sys.argv[3] if len(sys.argv)>3 else 'am,om,tl').split(',')
t=open(html,encoding='utf-8').read();dec=json.JSONDecoder()
def allR(t):
    i=t.index('const R=')+8;R,_=dec.raw_decode(t[i:])
    for m in re.finditer(r'R\.push\(',t):
        j=m.end()
        while True:
            o,e=dec.raw_decode(t[j:]);R.append(o);j+=e
            if t[j]==',':j+=1;continue
            break
    return R
ETH={}
m=re.search(r'/\*ETH\*/const ETH=',t)
if m: ETH={int(k):v for k,v in dec.raw_decode(t[m.end():])[0].items()}
lines=[];ids=[]
for r in allR(t):
    e=ETH.get(r['id'],{})
    if all(e.get(l) for l in LANGS): continue
    ids.append(r['id']);en=r['L']['en'];lines.append(f"@{r['id']} | {en['t']}")
    for b in en['blocks']:
        if b['t']=='note':continue
        lines.append(('= ' if b['t']=='ing' else '+ ')+b['h'])
        lines+=[('- ' if b['t']=='ing' else '> ')+x for x in b['items']]
    lines.append('')
open(out,'w',encoding='utf-8').write('\n'.join(lines))
print('missing',ids)
for l in LANGS: print(' ',l,'missing',[i for i in ids if not ETH.get(i,{}).get(l)])
