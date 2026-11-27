import sys,re
def struct(f):
    out=[];cur=None
    for l in open(f):
        l=l.rstrip('\n')
        if not l.strip(): continue
        k=l[0]
        if k=='@': cur=[l.split('|')[0].strip()];out.append(cur)
        else: cur.append(k)
    return out
a=struct(sys.argv[1]);b=struct(sys.argv[2])
ok=True
if len(a)!=len(b): print('recipe count',len(a),len(b));ok=False
for x,y in zip(a,b):
    if x!=y:
        ok=False;print('MISMATCH',x[0],y[0])
        for i,(p,q) in enumerate(zip(x,y)):
            if p!=q: print('  at',i,p,q);break
        print('  len',len(x),len(y))
print('OK' if ok else 'FAIL')
