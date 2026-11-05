"""Check the active architecture source graph and candidate traceability."""
from pathlib import Path
import json, re
b=Path(__file__).resolve().parent
root=b/'mbsManual.tex'
active={root}
def authored(text):
    text=re.sub(r'(?m)(?<!\\)%.*$', '', text)
    return re.sub(r'\\begin\{(?:verbatim|lstlisting)\}.*?\\end\{(?:verbatim|lstlisting)\}', '', text, flags=re.S)
def visit(p):
    text=authored(p.read_text())
    for path in re.findall(r'\\(?:include|input)\{([^{}]+)\}',text):
        target=b/(path if Path(path).suffix else path+'.tex')
        assert target.exists(), (p.name,path)
        if target not in active:
            active.add(target); visit(target)
visit(root)
joined='\n'.join(authored(p.read_text()) for p in active)
assert r'\newcommand{\FileNamespace}{mbs}' in joined
assert not re.search(r'(?m)^\s*\\includeonly\{',root.read_text())
for p in active:
    assert p.name.startswith('mbs'),p
    for path in re.findall(r'\\input\{(TikZ/[^}]+)\}',authored(p.read_text())):
        assert Path(path).parent.name==p.stem,(p,path)
        assert Path(path).name.startswith('mbs'),path
# Definitions and references in active source (not archived examples).
counts={}
for kind in ['UserStory','Requirement','UseCase','Architecture','TestCase','Verification','Validation']:
    defs=re.findall(r'\\'+kind+r'ID\{([^{}]+)\}',joined)
    refs=re.findall(r'\\'+kind+r'Ref\{([^{}]+)\}',joined)
    assert len(defs)==len(set(defs)),(kind,'duplicate ID')
    assert set(refs)<=set(defs),(kind,set(refs)-set(defs))
    counts[kind]=len(defs)
for n in range(101,107):
    rid=('REQ-F-'+str(n)) if n<=103 else ('REQ-C-'+str(n-3))
    test='TC-'+str(n); ver='VER-'+str(n)
    for filename,needle in [('mbsRequirements.tex',rid),('mbsTests.tex',rid),('mbsVerification.tex',rid),('mbsTraceability.tex',rid),('mbsUserStories.tex',rid),('mbsUseCases.tex',rid),('mbsValidation.tex',rid)]:
        assert needle in (b/filename).read_text(),(filename,needle)
    for filename in ['mbsRequirements.tex','mbsTests.tex','mbsVerification.tex','mbsTraceability.tex','mbsUseCases.tex']:
        assert test in (b/filename).read_text(),(filename,test)
    assert ver in (b/'mbsVerification.tex').read_text()
for filename in ['mbsVerification.tex','mbsValidation.tex','mbsTestEvidence.tex','mbsRequirements.tex']:
    text=(b/filename).read_text()
    if filename=='mbsRequirements.tex': text=text.split(r'\section{Project Candidate Requirements}')[1]
    assert r'\StatusPass' not in text,filename
    assert not re.search(r'\\ReqStatusDone\s*&',text),filename
# Bibliography keys for every active citation.
bib=(b/'mbsReferences.bib').read_text(); keys=set(re.findall(r'@\w+\s*\{\s*([^,]+)',bib))
for cite in re.findall(r'\\cite\{([^}]+)\}',joined):
    assert set(cite.split(','))<=keys,cite
report={'result':'PASS','active_tex_files':len(active),'active_tikz_files':sum('TikZ' in p.parts for p in active),'artifact_counts':counts,'checks':['all active inputs exist','mbs namespace and TikZ owner paths','no active includeonly','artifact IDs unique and references defined','six requirement/test/verification mappings reciprocal','no fabricated product pass or completed requirement','active bibliography citations resolve']}
print(json.dumps(report,indent=2))
