# Pre-commit reviewer hook for github-pr-reviewer project.
# Fires on any `git commit` shell command.
# Reads the staged diff, surfaces the reviewer.mdc checklist,
# and returns permission:"ask" so the user must confirm before proceeding.

$inputRaw = [Console]::In.ReadToEnd()
$inputJson = $inputRaw | ConvertFrom-Json -ErrorAction SilentlyContinue
$command   = if ($inputJson -and $inputJson.command) { $inputJson.command } else { "" }

# Only intercept git commit commands (not --no-verify bypass)
if ($command -notmatch "git\s+commit") {
    Write-Output '{"permission":"allow"}'
    exit 0
}

# Gather staged diff stats (last 15 lines to keep message concise)
$diffStat = ""
try {
    $rawStat = & git diff --staged --stat 2>$null
    if ($rawStat) {
        $diffStat = ($rawStat | Select-Object -Last 15) -join "`n"
    } else {
        $diffStat = "(no staged changes detected — did you git add?)"
    }
} catch {
    $diffStat = "(could not read staged diff)"
}

$message = @"
REVIEWER CHECKLIST (reviewer.mdc) — confirm all items before committing:

ARCHITECTURE LAYERS
  [ ] Routes are thin: parse input -> call use case -> return DTO (no business logic)
  [ ] domain/ and application/ have zero imports from infrastructure/, fastapi, sqlalchemy
  [ ] All DB access goes through infrastructure/db/repositories/ only
  [ ] All Gemini calls go through infrastructure/ai/gemini_client.py only

SECURITY
  [ ] No hardcoded secrets, API keys, or tokens anywhere
  [ ] Webhook route validates X-Hub-Signature-256 before processing
  [ ] All non-public API routes protected by auth_middleware.py

AGENTS / LANGGRAPH
  [ ] Agent nodes are pure state transformers — no side effects inside agent logic
  [ ] All Gemini calls use structured output (Pydantic schema, not json.loads)
  [ ] New agent node has @trace_agent decorator

CODE QUALITY
  [ ] All I/O is async (no time.sleep, no sync SQLAlchemy, no requests library)
  [ ] No print() — use structlog with job_id + repo + pr_number context
  [ ] Error responses use locked shape: {"error": {"code": "...", "message": "...", "details": {}}}
  [ ] ruff + mypy pass / tsc + eslint pass

TESTS
  [ ] New use case has unit test with mocked interfaces
  [ ] New API route has happy-path + unauthenticated integration tests
  [ ] pytest / vitest pass

STAGED CHANGES:
$diffStat
"@

$result = [PSCustomObject]@{
    permission    = "ask"
    user_message  = $message
    agent_message = "Pre-commit hook: reviewer.mdc checklist must pass. Staged diff shown above."
} | ConvertTo-Json -Compress -Depth 3

Write-Output $result
exit 0
