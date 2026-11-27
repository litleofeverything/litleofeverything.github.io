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
for lang in ('am','om'):
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
missing=[i for i in R if not ETH.get(i,{}).get('am') or not ETH.get(i,{}).get('om')]
print('recipes',len(R),'translated',len(R)-len(missing),'missing',missing)
data='const ETH='+json.dumps(ETH,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\nR.forEach(r=>{const e=ETH[r.id];if(e){if(e.am)r.L.am=e.am;if(e.om)r.L.om=e.om}});\n'
# remove old injected block if present
t=re.sub(r'/\*ETH\*/.*?/\*ETHEND\*/\n?','',t,flags=re.S)
anchor="let ulang=store.get('hr_lang',"
assert anchor in t
t=t.replace(anchor,'/*ETH*/'+data+'/*ETHEND*/\n'+anchor,1)
def once(old,new,key=None):
    global t
    if new in t or (key and key in t): return
    assert old in t,old[:60]
    t=t.replace(old,new,1)
once("const L=ulang==='hi'?{t:r.hi0,blocks:r.B0}:r.L[ulang];","const L=ulang==='hi'?{t:r.hi0,blocks:r.B0}:(r.L[ulang]||r.L.en);")
once("hi:{ing:'सामग्री',st:'बनाने का तरीका'}};","hi:{ing:'सामग्री',st:'बनाने का तरीका'},am:{ing:'ግብዓቶች',st:'አዘገጃጀት'},om:{ing:'Wantoota barbaachisan',st:'Qophii'}};")
once("const lang=s=>/[ঀ-৿]/.test(s)?'bn'","const lang=s=>/[\\u1200-\\u137F]/.test(s)?'am':/[ঀ-৿]/.test(s)?'bn'")
once("<button type=\"button\" data-lang=\"hi\">هندي</button></div>","<button type=\"button\" data-lang=\"hi\">هندي</button><button type=\"button\" data-lang=\"am\">أمهري</button><button type=\"button\" data-lang=\"om\">أورومو</button></div><select class=\"langsel\" aria-label=\"لغة الوصفات\"><option value=\"ar\">عربي</option><option value=\"en\">English</option><option value=\"hi\">هندي</option><option value=\"am\">أمهري</option><option value=\"om\">أورومو</option></select>")
once("hi:'الوصفات بالهندي'}[ulang])","hi:'الوصفات بالهندي',am:'የምግብ አዘገጃጀቶች በአማርኛ',om:'Qophiiwwan Afaan Oromootiin'}[ulang])")
once("document.querySelectorAll('[data-lang]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lang===ulang))}","document.querySelectorAll('[data-lang]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lang===ulang));const ls=document.querySelector('.langsel');if(ls)ls.value=ulang}")
once("r.L.en.blocks].flatMap(","r.L.en.blocks,...(r.L.am?[r.L.am.blocks]:[]),...(r.L.om?[r.L.om.blocks]:[])].flatMap(")
once("addEventListener('hashchange',ro","document.querySelector('.langsel').addEventListener('change',e=>{const b=document.querySelector('.langs [data-lang=\"'+e.target.value+'\"]');if(b)b.click()});\naddEventListener('hashchange',ro",".langsel').addEventListener('change'")
once("family=Hind+Siliguri:wght@400;600&","family=Hind+Siliguri:wght@400;600&family=Noto+Sans+Ethiopic:wght@400;600;700&")
css=""".langsel{display:none;height:34px;border:1px solid var(--line);border-radius:99px;background:var(--bg,#fff);color:var(--ink);font:inherit;font-size:14px;font-weight:600;padding:0 12px;margin-inline-end:6px}
[lang=am]{font-family:"Noto Sans Ethiopic","Nyala","Abyssinica SIL",sans-serif}
@media(max-width:600px){.langs{display:none}.langsel{display:block;height:32px;font-size:13px;padding:0 8px}}
</style>"""
if '.langsel{display:none' not in t:
    i=t.rindex('</style>');t=t[:i]+css+t[i+8:]
open(html_path,'w',encoding='utf-8').write(t)
print('ok')
