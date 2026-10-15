"""Focused independent decoder regression check; no candidate imports."""
import json
from pathlib import Path
import subprocess
import sys

candidate = Path(__file__).resolve().parents[2] / 'work/algorithm.py'
expected = {'n':7, 'edges':sorted([[0,2],[0,4],[0,6],[1,4],[1,6],[2,3],[2,5],[3,6],[4,5]]), 'bundles':[[1],[2],[3],[4],[5],[6],[0]]}
long_number = '9' * 5000
larger_number = '7' * 10000
cases = {
    'reported_integer': '{"n":'+long_number+',"edges":[],"lists":[]}',
    'negative_integer': '{"n":-'+long_number+',"edges":[],"lists":[]}',
    'oversized_edge_endpoint': '{"n":1,"edges":[[0,'+larger_number+']],"lists":[[1]]}',
    'oversized_color': '{"n":1,"edges":[],"lists":[['+larger_number+']]}',
    'nested_array': '['*30000 + '0' + ']'*30000,
    'truncated_nested_array': '['*30000 + '0',
    'numeric_exponent': '{"n":1e10000,"edges":[],"lists":[]}',
    'trailing_json': '{"n":0,"edges":[],"lists":[]} null',
}
for name, raw in cases.items():
    run = subprocess.run([sys.executable,str(candidate)], input=raw, text=True, capture_output=True)
    assert run.returncode == 0, (name, run.stderr)
    assert json.loads(run.stdout) == expected, (name,run.stdout)
source = {'n':1,'edges':[],'lists':[[3]]}
run = subprocess.run([sys.executable,str(candidate)],input=json.dumps(source),text=True,capture_output=True,check=True)
target = json.loads(run.stdout)
witness = [3,1,1,2,2,3,3]
assert all(witness[u]!=witness[v] for u,v in target['edges'])
assert sum(w*max(witness[v] for v in b) for w,b in zip([4096,1024,256,64,16,4,1],target['bundles'])) == 5823
run = subprocess.run([sys.executable,str(candidate),'--extract'],input=json.dumps({'source':source,'target_solution':witness}),text=True,capture_output=True,check=True)
assert json.loads(run.stdout) == [3]
print(json.dumps({'python':sys.version,'fixed_no_checks':list(cases),'passed':len(cases),'legal_forward_and_recovery':'passed'},indent=2))
