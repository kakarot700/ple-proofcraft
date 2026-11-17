import ast,re,unittest
from pathlib import Path
m=ast.parse(Path(__file__).with_name("serve.py").read_text())
f=next(n for n in m.body if isinstance(n,ast.FunctionDef) and n.name=="should_continue_work")
ns={"re":re};exec(compile(ast.Module(body=[f],type_ignores=[]),"gate","exec"),ns)
class GuardTest(unittest.TestCase):
 def test_unfinished(self):
  self.assertTrue(ns["should_continue_work"]("Let me debug.",18000,180))
 def test_finished(self):
  self.assertFalse(ns["should_continue_work"]("Completed and verified.",18000,180))
 def test_deadline(self):
  self.assertFalse(ns["should_continue_work"]("I will debug.",600,180))
if __name__=="__main__": unittest.main()
