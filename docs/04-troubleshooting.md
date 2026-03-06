# Troubleshooting Operations

This document compiles the most frequent errors engineers face when operating the containerized ETL pipeline locally, outlining the specific cause and the recommended fix.

---

## 1. Environment Build Fails: "ModuleNotFoundError: No module named 'src'"

**Symptom:**
When executing `docker compose run --rm etl pytest`, the Python interpreter fatally crashes claiming it cannot find the `src.extract...` directories.

**The Cause (Why this happens):**
Python inherently struggles with relative import paths during testing if it doesn't clearly recognize the project root. Pytest assumes the root is exactly where the test file is located, failing to look "up" a directory.

**The Fix:**
You must configure the test suite's environment correctly so it recognizes `src/` locally. We achieve this by adding `tests/conftest.py` which explicitly modifies Python's native `sys.path` variable to include the direct parent root before any test executes.

---

## 2. Authentication Block: "Invalid Credentials" in JupyterLab

**Symptom:**
Opening Jupyter on `localhost:8888` continually demands a password. The `JUPYTER_TOKEN` you passed into `.env` is universally rejected over the UI.

**The Cause (Why this happens):**
Your token wasn't structurally loaded by Docker during boot. The container might have been spawned directly with a raw CMD block that failed to extrapolate the operating system's `$JUPYTER_TOKEN` variable into string text.

**The Fix:**
1. Execute `docker exec -it pde_jupyter_lab jupyter server list`.
2. Inspect the generated output. If the list physically says `token=lsJUPYTER_TOKEN` or a similarly malformed string instead of the value in your `.env` file, the container interpolation failed.
3. Guarantee that the Docker Compose `command` for the jupyter service explicitly utilizes shell wrapping: `command: ["sh", "-lc", "jupyter lab ..."]`.
4. If the error persists, completely strip down the old containers using `docker compose down -v` and cleanly boot them via `docker compose up -d`.

---

## 3. Configuration Load Block: "`pytest.ini` unexpected line: '\ufeff[pytest]'"

**Symptom:**
Pytest halts execution immediately: `ERROR: /app/pytest.ini:1: unexpected line: '\ufeff[pytest]'`.

**The Cause (Why this happens):**
Windows file management! You likely created the `pytest.ini` file using Notepad or a similar Windows raw editor that stealthily injected a "UTF-8 BOM" (Byte Order Mark) invisibly to the start of the file. Pytest expects pure unformatted Unix text and chokes on the hidden UTF-8 signature characters.

**The Fix:**
Open the file in VS Code or any strict IDE. In the very bottom right-hand corner, change the file encoding type from `UTF-8 with BOM` precisely back to pure `UTF-8` and explicitly save the file.

---

## 4. Compose Failures: "Project not found" after renaming folder

**Symptom:**
You renamed your local folder containing the project on your laptop (e.g. from `de-lab-001` to `de-lab-fraud`). When executing `docker compose ps` nothing appears; the shell falsely claims there are no running containers.

**The Cause (Why this happens):**
Docker Compose intrinsically ties deployment instances to the exact name of the encompassing folder by default. If you rename the underlying folder, Docker Compose believes you are in an entirely new codebase and "loses track" of the previously spun-up background containers.

**The Fix:**
You must explicitly point docker to shut down your old project identifiers before attempting to boot the new folder.
```bash
docker compose -p <old_project_name> down
docker compose up -d
```

---

## 5. Storage Blocks: "used by another process" (Windows specific)

**Symptom:**
When explicitly renaming directories or attempting to delete large folders via PowerShell, Windows blocks execution quoting: `The process cannot access the file because it is being used by another process.`

**The Cause (Why this happens):**
A raw script, file explorer UI, or internal IDE indexing engine is fundamentally tracking files inside the directory, locking the overall filesystem operation to prevent corruption.

**The Fix:**
1. Ensure no terminal is definitively `.cd`'d into the local folder. 
2. Shut down Docker volumes tied to the directory.
3. If deeply locked, load `resmon` (Windows Resource Monitor), hit the CPU tab -> Associated Handles -> search for the file identifier to forcibly identify and terminate the tracking process.
