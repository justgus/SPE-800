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

# Derive trace relationships from authored rows; do not hard-code artifact counts.
def rows(filename, kind):
    text=authored((b/filename).read_text())
    return dict(re.findall(r'\\'+kind+r'ID\{([^{}]+)\} & ([^\n]+)',text))
def references(text,kind):
    return set(re.findall(r'\\'+kind+r'Ref\{([^{}]+)\}',text))
requirements=rows('mbsRequirements.tex','Requirement')
tests=rows('mbsTests.tex','TestCase')
stories=rows('mbsUserStories.tex','UserStory')
verification=rows('mbsVerification.tex','Verification')
validation=rows('mbsValidation.tex','Validation')
usecases=authored((b/'mbsUseCases.tex').read_text())
case_blocks={}
for part in usecases.split(r'\caption{')[1:]:
    match=re.search(r'\\UseCaseID\{([^{}]+)\}',part)
    if match: case_blocks[match[1]]=part
trace=authored((b/'mbsTraceability.tex').read_text())
assert len(requirements)==counts['Requirement'], 'unparsed requirement rows'
assert len(tests)==counts['TestCase'], 'unparsed test rows'
assert len(stories)==counts['UserStory'], 'unparsed story rows'
assert len(case_blocks)==counts['UseCase'], 'unparsed use cases'
assert len(verification)==counts['Verification'], 'unparsed verification rows'
assert len(validation)==counts['Validation'], 'unparsed validation rows'
for rid,row in requirements.items():
    tc=references(row,'TestCase'); us=references(row,'UserStory'); uc=references(row,'UseCase')
    assert tc and us and uc,(rid,'missing mapping')
    for tid in tc:
        assert tid in tests and rid in references(tests[tid],'Requirement'),(rid,tid)
        assert references(tests[tid],'UseCase')==uc,(rid,tid,'case mismatch')
    for sid in us:
        assert sid in stories and rid in references(stories[sid],'Requirement'),(rid,sid)
    for cid in uc:
        assert cid in case_blocks and rid in references(case_blocks[cid],'Requirement'),(rid,cid)
        assert tc<=references(case_blocks[cid],'TestCase'),(rid,cid,'test gap')
    vv=[(vid,vrow) for vid,vrow in verification.items() if rid in references(vrow,'Requirement')]
    assert len(vv)==1 and references(vv[0][1],'TestCase')==tc,(rid,'verification gap')
    matching=[line for line in trace.splitlines() if r'\RequirementRef{'+rid+'} &' in line]
    assert len(matching)==1,(rid,'trace row')
    tr=matching[0]
    assert references(tr,'UserStory')==us and references(tr,'UseCase')==uc and references(tr,'TestCase')==tc,(rid,'trace mismatch')
    assert references(tr,'Verification')=={vv[0][0]} and references(tr,'Architecture'),(rid,'design/evidence gap')
    vl=references(tr,'Validation'); assert vl,(rid,'missing validation')
    for sid in us:
        assert any(vid in validation and sid in references(validation[vid],'UserStory') and rid in references(validation[vid],'Requirement') and tc<=references(validation[vid],'TestCase') for vid in vl),(rid,sid,'validation gap')
for tid,trow in tests.items():
    assert references(trow,'Requirement'),(tid,'orphan test')
    for rid in references(trow,'Requirement'):
        assert rid in requirements and tid in references(requirements[rid],'TestCase'),(tid,rid,'reverse test gap')
for filename in ['mbsVerification.tex','mbsValidation.tex','mbsTestEvidence.tex','mbsRequirements.tex']:
    text=(b/filename).read_text()
    if filename=='mbsRequirements.tex': text=text.split(r'\section{Project Candidate Requirements}')[1]
    assert r'\StatusPass' not in text,filename
    assert not re.search(r'\\ReqStatusDone\s*&',text),filename
# Bibliography keys for every active citation.
bib=(b/'mbsReferences.bib').read_text(); keys=set(re.findall(r'@\w+\s*\{\s*([^,]+)',bib))
for cite in re.findall(r'\\cite\{([^}]+)\}',joined):
    assert set(cite.split(','))<=keys,cite
report={'result':'PASS','active_tex_files':len(active),'active_tikz_files':sum('TikZ' in p.parts for p in active),'artifact_counts':counts,'checks':['all active inputs exist','mbs namespace and TikZ owner paths','no active includeonly','artifact IDs unique and references defined',str(len(requirements))+' requirement mappings reciprocal across all seven registers','no fabricated product pass or completed requirement','active bibliography citations resolve']}
print(json.dumps(report,indent=2))
