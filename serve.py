# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ProofCraft WebSocket entrypoint.

The harness itself (agent loop, tool dispatch, engineering policy and the
completion/verification gates) lives in ``harness.py``. This module only wires
it to the PLE task bridge and serves the protocol the evaluator speaks.
"""

import taskbridge
from harness import *  # noqa: F401,F403  (the harness's own module-level names)
from harness import Agent  # noqa: F401

async def solve(session: taskbridge.Session) -> str:
  """Runs `Agent` on `session` and returns the final answer.

  Args:
    session: Active task session.

  Returns:
    The final summary string returned by the agent.
  """
  print(
      f"task: workdir {session.workdir}, model {MODEL},"
      f" {len(session.mcp_servers)} MCP server(s)",
      file=sys.stderr,
  )
  return await Agent(session).run()


if __name__ == "__main__":
  taskbridge.run(solve)
