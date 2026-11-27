import sys,re,json,glob,os
html_path=sys.argv[1]
t=open(html_path,encoding='utf-8').read()
dec=json.JSONDecoder()
def allR(t):
    i=t.index('const R=')+8
    R,_=dec.raw_decode(t[i:])
    for m in re.finditer(r'R\.push\(',t):
        j=m.end()
        while True:
            o,e=dec.raw_decode(t[j:]);R.append(o);j+=e
            if t[j]==',':j+=1;continue
            break
    return R
R={r['id']:r for r in allR(t)}
def parse(f):
    out={};cur=None;blk=None
    for l in open(f,encoding='utf-8'):
        l=l.rstrip('\n')
        if not l.strip():continue
        k=l[0];x=l[2:].strip() if len(l)>1 else ''
        if k=='@':
            rid,title=l[1:].split('|',1);cur={'t':title.strip(),'blocks':[]};out[int(rid)]=cur
        elif k in '=+':
            blk={'t':'ing' if k=='=' else 'step','h':x,'items':[]};cur['blocks'].append(blk)
        elif k in '->':blk['items'].append(x)
    return out
TDIR=sys.argv[2] if len(sys.argv)>2 else os.path.dirname(os.path.abspath(__file__))
ETH={}
_m=re.search(r'/\*ETH\*/const ETH=',t)
if _m:
    _o,_=dec.raw_decode(t[_m.end():])
    ETH={int(k):v for k,v in _o.items()}
LANGS=('am','om','tl')
for lang in LANGS:
    for f in sorted(glob.glob(os.path.join(TDIR,f'{lang}_*.txt'))):
        for rid,d in parse(f).items():
            r=R.get(rid)
            if not r: continue
            en=[b for b in r['L']['en']['blocks'] if b['t']!='note']
            assert len(en)==len(d['blocks']),(lang,rid)
            for a,b in zip(en,d['blocks']):
                assert a['t']==b['t'] and len(a['items'])==len(b['items']),(lang,rid,a.get('h'))
                if 'ha' in a: b['ha']=a['ha']
                if 'ia' in a: b['ia']=a['ia']
            ETH.setdefault(rid,{})[lang]=d
missing=[i for i in R if any(not ETH.get(i,{}).get(l) for l in LANGS)]
print('recipes',len(R),'translated',len(R)-len(missing),'missing',missing)
# Replace only the ETH data object; the language UI is already in the page.
m=re.search(r'/\*ETH\*/const ETH=',t)
assert m,'ETH block not found in page'
_,n=dec.raw_decode(t[m.end():])
js=json.dumps({str(k):ETH[k] for k in ETH},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
t=t[:m.end()]+js+t[m.end()+n:]
open(html_path,'w',encoding='utf-8').write(t)
print('ok')
