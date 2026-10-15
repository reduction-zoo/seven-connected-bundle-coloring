"""Regression of malformed-string totality without importing candidate code."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

work = Path(__file__).resolve().parents[2] / 'work'
spec = importlib.util.spec_from_file_location('prepared', work / 'check.py')
prepared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepared)
cases = {
    'large-positive-count': '{"n":' + '9' * 5000 + ',"edges":[],"lists":[]}',
    'large-negative-count': '{"n":-' + '1' * 5000 + ',"edges":[],"lists":[]}',
    'large-list-color': '{"n":1,"edges":[],"lists":[[' + '1' * 5000 + ']]}',
    'deep-array': '[' * 20000 + '0' + ']' * 20000,
    'truncated-object': '{"n":',
    'trailing-values': '{} {}',
    'out-of-range-edge': '{"n":1,"edges":[[0,1]],"lists":[[1]]}',
    'boolean-count': '{"n":true,"edges":[],"lists":[[1]]}',
}
for name, raw in cases.items():
    result = subprocess.run([sys.executable, str(work / 'algorithm.py')],
                            input=raw, text=True, capture_output=True, check=True)
    output = json.loads(result.stdout)
    assert prepared.valid_target(output), name
    assert not prepared.solve(output, target=True), name
print(json.dumps({'cases':list(cases), 'legal_no_outputs':len(cases), 'python':sys.version}))
