"""Live Groq integration, not a PLE benchmark or official kit check."""
import asyncio, os, pathlib, tempfile, time, json, subprocess
os.environ.update(MODEL_NAME='openai/gpt-oss-120b',MODEL_BASE_URL='https://api.groq.com/openai/v1',MODEL_API_KEY=pathlib.Path('/tmp/ple-secrets/groq.key').read_text().strip(),MAX_OUTPUT_TOKENS='2048')
import serve
class LocalSession:
 def __init__(self,workdir):
  self.workdir=workdir; self.instruction='Create hello.txt containing exactly HELLO followed by a newline. Do not create other files. Then reply done.';self.mcp_servers=[];self.limits={'exec_timeout_sec':30};self.final_message=''; self.end=time.monotonic()+50;self.calls=[];self.tokens=[]
 def time_left(self):return self.end-time.monotonic()
 async def log(self,msg):self.calls.append(msg)
 async def usage(self,*args):self.tokens.append(args)
 async def write_file(self,path,content,append=False):
  p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
  if not (p.resolve().is_relative_to(pathlib.Path(self.workdir).resolve()) or str(p).startswith('/tmp/proofcraft/')):
   raise ValueError(f'write outside workdir: {path}')
  p.write_text(content) if not append else p.write_text((p.read_text() if p.exists() else '')+content);return p.stat().st_size
 async def read_file(self,path):return pathlib.Path(path).read_bytes()
 async def exec(self,command,timeout):
  p=await asyncio.create_subprocess_exec('bash','-lc',command,cwd=self.workdir,stdout=-1,stderr=-2)
  try: out,_=await asyncio.wait_for(p.communicate(),timeout)
  except asyncio.TimeoutError:p.kill();await p.wait();return {'exit_code':-9,'output':'timeout','timed_out':True}
  return {'exit_code':p.returncode,'output':out.decode()}
async def main():
 with tempfile.TemporaryDirectory(prefix='ple-smoke-') as d:
  s=LocalSession(d);answer=await serve.solve(s);p=pathlib.Path(d)/'hello.txt';ok=p.exists() and p.read_bytes()==b'HELLO\n' and len(list(pathlib.Path(d).iterdir()))==1
  result={'test':'live integration only, not benchmark','passed':ok,'answer':answer,'calls':s.calls,'usage':s.tokens};print(json.dumps(result,indent=2));pathlib.Path('/tmp/ple-live-smoke.json').write_text(json.dumps(result,indent=2));assert ok
asyncio.run(main())
