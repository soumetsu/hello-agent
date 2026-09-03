# Project Rules

## Scope

- Keep the application split between `backend/` (FastAPI) and `frontend/`
  (Vue).
- Put backend application code under `backend/app/`.
- Put frontend application code under `frontend/src/`.
- Keep changes focused on the requested feature; avoid unrelated rewrites.

## Backend conventions

- Use Python type hints for public functions and route handlers.
- Prefer small modules grouped by responsibility as the API grows.
- Keep API responses JSON-serializable and document new endpoints.
- Add tests for new backend behavior before considering a feature complete.

## Frontend conventions

- Use Vue Single-File Components and the Composition API.
- Keep reusable components focused and place them under
  `frontend/src/components/` when introduced.
- Keep global styling minimal; colocate component-specific styles with their
  components.
- Ensure user-facing controls are keyboard accessible and clearly labeled.

## Dependencies and configuration

- Do not add or install a dependency unless the task requires it.
- Document newly required environment variables in an `.env.example` file.
- Never commit credentials, API keys, virtual environments, `node_modules/`, or
  generated build output.
- Update `README.md` whenever setup steps or required tooling change.

## Verification

- Run relevant backend and frontend checks after changing code.
- Do not claim checks passed unless they were actually run.
- Report any checks that could not run because dependencies are not installed.

## Course macros

### AutoLoop

Trigger: When the user says **"AutoLoop"**, perform a bounded fix-and-verify
loop.

1. Read `AGENTS.md`, `README.md`, and the relevant verification instructions.
2. State the acceptance check for the current task.
3. Run the smallest relevant check.
4. If the check fails for an in-scope source-code reason, inspect the evidence,
   make the smallest relevant correction, and rerun the check.
5. Repeat for no more than five correction cycles.
6. Stop early and ask for direction if the next action requires a dependency
   change, machine-level permission, destructive action, an unrelated process
   to be stopped, or broader scope.
7. Report every cycle, the final evidence, and anything not verified.

### SmokeTest

Trigger: When the user says **"Run the smoke test"**, verify the working
application without changing source code or dependency declarations.

1. Read `AGENTS.md`, `README.md`, and `docs/verification.md`.
2. Run the backend pytest suite.
3. Run the frontend lint and production build.
4. Check the intended backend and frontend ports. Never stop an unrelated
   process.
5. Start only the backend and frontend processes needed for this test in
   Codex-managed terminals.
6. Verify one successful API request and division-by-zero handling.
7. Use automated browser control to operate the visible calculator. Enter `7`
   and `6`, exercise all four operation buttons, and confirm the displayed
   results: Add is `13`, Subtract is `1`, Multiply is `42`, and Divide is
   `1.1666666666666667`.
8. Exercise both clearing behaviors. Confirm **Clear inputs** empties the two
   inputs while preserving the selected operation and last feedback. Confirm
   **Reset calculator** restores `0` and `0`, selects Add, and clears result and
   error feedback. Also confirm that the browser displays no unexpected
   application error and report any UI behavior that could not be tested.
9. Unless the user asks to keep the app running, stop only the processes
   created by this smoke test.
10. Report concise evidence from tests, builds, endpoints, the automated UI
    interaction, and service cleanup.

### Combined trigger

When the user says **"AutoLoop: run the smoke test"**, run the SmokeTest macro.
If an in-scope check fails, use the AutoLoop rules to make the smallest
correction and repeat the smoke test until it passes, five correction cycles
are exhausted, or a stopping condition is reached.
