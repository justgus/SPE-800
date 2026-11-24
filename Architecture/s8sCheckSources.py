"""Check the active architecture source graph and candidate traceability."""
from pathlib import Path
import json, re
b=Path(__file__).resolve().parent
root=b/'s8sManual.tex'
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
# Check every reader-facing internal target after publication scope changes.
labels=set(re.findall(r'\\label\{([^{}]+)\}',joined))
labels.update('Chapter:'+v for v in re.findall(r'\\ChapterLabel\{([^{}]+)\}',joined))
for kind in ['UserStory','Requirement','UseCase','Architecture','TestCase','Verification','Validation']:
    labels.update(kind+':'+v for v in re.findall(r'\\'+kind+r'ID\{([^{}]+)\}',joined))
targets=set(re.findall(r'\\(?:hyperref|hyperlink)\[([^\]]+)\]',joined))
targets.update(re.findall(r'\\(?:ref|pageref|autoref)\*?\{([^{}]+)\}',joined))
targets.update('Chapter:'+v for v in re.findall(r'\\ChapterRef\{([^{}]+)\}',joined))
assert targets<=labels, ('unresolved publication targets', sorted(targets-labels))
assert r'\newcommand{\FileNamespace}{s8s}' in joined
assert not re.search(r'(?m)^\s*\\includeonly\{',root.read_text())
for p in active:
    assert p.name.startswith('s8s'),p
    for path in re.findall(r'\\input\{(TikZ/[^}]+)\}',authored(p.read_text())):
        assert Path(path).parent.name==p.stem,(p,path)
        assert Path(path).name.startswith('s8s'),path
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
requirements=rows('s8sRequirements.tex','Requirement')
tests=rows('s8sTests.tex','TestCase')
stories=rows('s8sUserStories.tex','UserStory')
verification=rows('s8sVerification.tex','Verification')
validation=rows('s8sValidation.tex','Validation')
usecases=authored((b/'s8sUseCases.tex').read_text())
case_blocks={}
for part in usecases.split(r'\caption{')[1:]:
    match=re.search(r'\\UseCaseID\{([^{}]+)\}',part)
    if match: case_blocks[match[1]]=part
trace=authored((b/'s8sTraceability.tex').read_text())
primary_trace=trace.split(r'\section{Supporting Trace Links}')[0]
for line in primary_trace.splitlines():
    if line.startswith((r'\UserStoryRef{',r'\RequirementRef{')):
        assert line.startswith(r'\UserStoryRef{') and len(line.split(' & '))==4, ('malformed primary trace row',line)
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
    requirement_ref = r'\RequirementRef{' + rid + '}'
    matching = [line for line in trace.splitlines() if line.startswith(requirement_ref + ' &')]
    assert len(matching)==1,(rid,'trace row')
    tr=matching[0]
    assert references(tr,'UserStory')==us and references(tr,'UseCase')==uc and references(tr,'TestCase')==tc,(rid,'trace mismatch')
    assert references(tr,'Verification')=={vv[0][0]} and references(tr,'Architecture'),(rid,'design/evidence gap')
    matrix_rows = [line.split(' & ') for line in trace.splitlines()
                   if line.startswith(r'\UserStoryRef{') and references(line, 'Requirement') == {rid}]
    assert len(matrix_rows) == 1 and len(matrix_rows[0]) == 4, (rid, 'trace matrix row')
    story_cell, _, verification_cell, evidence_cell = matrix_rows[0]
    assert references(story_cell, 'UserStory') == us, (rid, 'trace matrix story mismatch')
    assert references(verification_cell, 'Verification') == {vv[0][0]}, (rid, 'trace matrix verification mismatch')
    assert evidence_cell.removesuffix(r'\\').strip(), (rid, 'missing pass evidence disposition')
    validation_rows = [(vid, row) for vid, row in validation.items()
                       if rid in references(row, 'Requirement')]
    assert len(validation_rows) == 1, (rid, 'expected one validation entry')
    vid, validation_row = validation_rows[0]
    assert references(tr, 'Validation') == {vid}, (rid, 'validation link mismatch')
    assert references(validation_row, 'Requirement') == {rid}, (rid, 'validation requirement mismatch')
    assert references(validation_row, 'UserStory') == us, (rid, 'validation story mismatch')
    assert references(validation_row, 'UseCase') == uc, (rid, 'validation use case mismatch')
    assert references(validation_row, 'TestCase') == tc, (rid, 'validation test mismatch')
for tid,trow in tests.items():
    assert references(trow,'Requirement'),(tid,'orphan test')
    for rid in references(trow,'Requirement'):
        assert rid in requirements and tid in references(requirements[rid],'TestCase'),(tid,rid,'reverse test gap')
for filename in ['s8sVerification.tex','s8sValidation.tex','s8sTestEvidence.tex','s8sRequirements.tex']:
    text=(b/filename).read_text()
    if filename=='s8sRequirements.tex': text=text.split(r'\section{Project Candidate Requirements}')[1]
    assert r'\StatusPass' not in text,filename
    assert not re.search(r'\\ReqStatusDone\s*&',text),filename
# Bibliography keys for every active citation.
bib=(b/'s8sReferences.bib').read_text(); keys=set(re.findall(r'@\w+\s*\{\s*([^,]+)',bib))
for cite in re.findall(r'\\cite\{([^}]+)\}',joined):
    assert set(cite.split(','))<=keys,cite
report={'result':'PASS','active_tex_files':len(active),'active_tikz_files':sum('TikZ' in p.parts for p in active),'artifact_counts':counts,'checks':['all active inputs exist','s8s namespace and TikZ owner paths','no active includeonly','artifact IDs unique and references defined',str(len(requirements))+' requirement mappings reciprocal across all seven registers','no fabricated product pass or completed requirement','active bibliography citations resolve']}
print(json.dumps(report,indent=2))
