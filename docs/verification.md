# Verification

Run commands from the project root unless a step says otherwise.

## Automated checks

Backend, from `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Frontend, from `frontend/`:

```powershell
npm run lint
npm run build
```

All commands must exit successfully. Report warnings separately from failures.

## Smoke test

- Confirm ports `8000` and `5173` are available. Do not stop an existing
  process using either port.
- Start FastAPI on `http://127.0.0.1:8000` from `backend/`:

  ```powershell
  .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
  ```

- Start Vue on `http://127.0.0.1:5173` from `frontend/`:

  ```powershell
  npm run dev -- --host 127.0.0.1
  ```

- Through the Vite proxy, verify a successful calculator request returns HTTP
  `200` with a JSON `result`, and division by zero returns HTTP `400` with
  `{"detail":"Cannot divide by zero."}`.
- In the browser, enter `7` and `6`. Exercise each operation button and confirm
  Add is `13`, Subtract is `1`, Multiply is `42`, and Divide is
  `1.1666666666666667`.
- Select **Clear inputs** and confirm both inputs are empty while the selected
  operation and last feedback remain. Select **Reset calculator** and confirm
  both inputs return to `0`, Add is selected, and result/error feedback is
  cleared.
- Confirm there is no unexpected application error.
- Stop only the FastAPI and Vite processes started for the smoke test unless the
  user asks to keep them running.
