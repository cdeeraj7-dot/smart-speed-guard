# Smart Speed Guard — Development Log

This log records observed repository history and verified work. Git commit
subjects below are reproduced as recorded; they are not substitutes for
reviewing the associated diffs.

## 2026-09-12 — Repository history

- Git history records `8fec7e5` — “Create project repository structure”.
- Git history records `1a8fa2d` — “Add Phase 2 AI and MCU foundation”.
- These entries indicate repository activity, not independent acceptance of
  every phase or hardware function.

## 2026-09-17 — Repository history

- Git history records `4ea11c7` — “Add verified MCU to Linux telemetry flow”.
- Git history records `ddb4bdb` — “Integrate real telemetry with AI preprocessing”.
- Git history records `e1c17c0` — “Add sensor-aware feature extraction”.
- Git history records `8be1303` — “Add telemetry monitoring dashboard”.

## 2026-11-03 — Repository history

- Git history records `c2f1e31` — “Integrate risk profiling and Arduino vision pipeline”.

## 2026-11-09 — Telemetry correction recorded in the prior work session

- MCU invalid accelerometer samples are zeroed rather than retaining stale
  values.
- `gyro_valid` is represented in MCU telemetry and forwarded through the
  Bridge payload to the Linux CSV schema.
- The MCU timestamp is retained as the telemetry timestamp.
- The receiver validates its CSV header against the current schema.
- The prior session reported 111 Python tests passing and Python syntax
  compilation passing. Those checks were rerun at the 2026-11-14 checkpoint
  below.
- MCU compilation and physical Bridge communication were not verified.

## 2026-11-14 — Recovery and progress checkpoint

- Inspected the repository state and confirmed that the architecture audit's
  “no source code” inventory conflicts with the current tree. The audit was
  not overwritten; reconciliation remains pending.
- The working tree contained uncommitted changes in:
  `firmware/linux/README.md`, `firmware/linux/receiver.py`,
  `firmware/mcu/include/telemetry.h`, `firmware/mcu/src/imu.cpp`,
  `firmware/mcu/src/main.cpp`, and `firmware/mcu/src/telemetry.cpp`.
- The changes in `firmware/mcu/src/imu.cpp` were not attributed to this
  checkpoint; inspect their diff before editing.
- Created `PROJECT_PROGRESS.md`, `DEVELOPMENT_LOG.md`, `NEXT_SESSION.md`,
  `PHASE_CHECKLIST.md`, and `CHANGELOG.md` because none existed at the
  repository root.
- Tests executed:
  - `.venv\Scripts\python.exe -m pytest` — **111 passed in 0.54s**.
  - `.venv\Scripts\python.exe -m compileall -q ai firmware tests` —
    **passed**.
- The source and receiver indicate a telemetry schema with `gyro_valid`, but
  no physical Bridge test or MCU compilation was available. No sensor values
  were fabricated and no hardware validation was claimed.
- No commit or push was made.

## 2026-11-14 — Stage 0 reconciliation started

- Reviewed the saved progress, next-session notes, phase checklist, latest
  development-log entry, Git state, and affected source files.
- Exact working-tree state at phase start: six modified tracked source/docs
  files plus the five new root checkpoint files. No changes were discarded.
- The pending `firmware/mcu/src/imu.cpp` diff changes I2C calls from `Wire2` to
  `Wire`; its origin and hardware correctness remain unknown, so it is
  explicitly out of scope.
- Planned work: update only stale statements in
  `docs/architecture/ARCHITECTURE_AUDIT.md`, refresh phase tracking, and verify
  the resulting documentation and diff.
- Acceptance: the audit inventory accurately reflects present source/test/
  dashboard files, distinguishes code presence from verified runtime or
  hardware behavior, and retains unresolved board/electrical/protocol
  decisions. Do not claim physical validation.
- Risks/dependencies: no authoritative board details or physical hardware
  evidence were provided. This phase will not resolve pin maps, compile
  firmware, alter the telemetry schema, or infer unimplemented sensor data.
- Python suite (111 passed) and syntax checks passed earlier on 2026-11-14;
  this documentation-only phase does not require rerunning them unless source
  changes are made.

## 2026-11-14 — Stage 0 completion and Stage 1 assessment

### Phase-completion report — Stage 0: Architecture audit reconciliation

- Completion date: 2026-11-14.
- Completed: corrected the audit's repository inventory to recognize partial
  MCU/Linux source, AI/preprocessing/tests, a dashboard app, the Python
  dependency manifest, and the actual offline test results.
- Files created during Stage 0: none.
- Files modified: `docs/architecture/ARCHITECTURE_AUDIT.md`,
  `PROJECT_PROGRESS.md`, `DEVELOPMENT_LOG.md`, `NEXT_SESSION.md`,
  `PHASE_CHECKLIST.md`, and `CHANGELOG.md`. No source implementation changed.
- Tests: documentation-only change; tests were not rerun. Latest verified
  result remains 111 Python tests passed and Python compileall passed earlier
  on 2026-11-14.
- Known defects: audit still lists unresolved board, electrical, transport,
  sensor ownership, thresholds, LTE, and acceptance questions; these are
  intentionally not fabricated.
- Deferred work: resolve those technical questions using authoritative
  documentation and available hardware.
- Hardware verification: none performed; expanded Bridge communication and MCU
  compilation remain unverified.
- Remaining risks: incorrect board/bus assumptions, absent MCU build workflow,
  unverified physical message path, and deadline handover.
- Next phase: Stage 1 — Repository structure and reproducible setup.

### Stage 1 start/assessment

- Reviewed existing project directories, Python dependency manifest, source
  inventory, and local Arduino installation.
- The user confirmed the UNO Q 2GB is available, Arduino IDE/App Lab is the
  intended toolchain, the MPU6050 is connected on `Wire`, and the existing
  `Wire2`-to-`Wire` edit is intentional and based on actual wiring.
- The bundled Arduino CLI was found (1.5.1); installed platform `arduino:zephyr`
  1.0.0 exposes FQBN `arduino:zephyr:unoq`; RouterBridge 0.4.3 is installed.
- The first compile attempt failed because the sketch root lacked `mcu.ino`.
- Added `firmware/mcu/mcu.ino` as the required sketch entry and
  `firmware/mcu/README.md` with the tested build command and versions.
- The build then passed with 96,224 bytes of program storage and 40,956 bytes
  of global variables reported by the compiler. This verifies compilation
  only, not flashing or physical behavior.
- Stage 1 acceptance is met for the documented CLI build setup; IDE GUI
  compilation and hardware operation have not been verified.
- No files were committed or pushed.

### Phase-completion report — Stage 1: Repository structure and build setup

- Completion date: 2026-11-14.
- Tasks completed: verified existing source/test organization, added the
  Arduino sketch entry, recorded the UNO Q CLI command, and compiled the MCU
  source for the installed UNO Q platform.
- Files created: `firmware/mcu/mcu.ino`, `firmware/mcu/README.md`.
- Files modified: `PROJECT_PROGRESS.md`, `DEVELOPMENT_LOG.md`,
  `NEXT_SESSION.md`, `PHASE_CHECKLIST.md`, `CHANGELOG.md`, and
  `docs/architecture/ARCHITECTURE_AUDIT.md`.
- Tests: Arduino CLI compile passed for FQBN `arduino:zephyr:unoq`; Python suite
  remains 111 passed and Python compileall passed from earlier on 2026-11-14.
- Known defects: source has not been flashed; no physical sensor or Bridge
  behavior was tested.
- Deferred work: IDE GUI build confirmation and hardware test.
- Hardware verification: board availability and `Wire` connection were
  user-confirmed; no electrical measurement/read test performed.
- Remaining risks: peripheral voltage/pin details, timing behavior, Bridge
  runtime behavior, and safety acceptance criteria.
- Next phase: Stage 2 — MCU foundation.

### Stage 2 start checkpoint

- Previous phase acceptance: Stage 1's CLI build setup compiled successfully.
- Starting state: all pre-existing worktree changes are preserved; the current
  MCU loop has a fixed `delay(500)` after telemetry transmission.
- Planned task: replace only that fixed wait with elapsed-time scheduling,
  retaining immediate first transmission and a 500 ms minimum interval.
- Dependencies: Arduino `millis()`/UNO Q core, already used elsewhere in the
  sketch; no new library or hardware assumption.
- Risks: `Bridge.call()` and serial/I2C operations may themselves block; this
  change does not claim hard real-time timing or measured latency.
- Acceptance: compile for UNO Q; keep sensor payload, timestamps, safety logic,
  and thresholds unchanged.

### Stage 2 module checkpoint — telemetry loop cadence

- Replaced the fixed `delay(500)` in `firmware/mcu/src/main.cpp` with an
  unsigned elapsed-time check using `millis()`.
- First telemetry cycle still runs immediately; subsequent cycles are gated by
  500 ms elapsed from the previous cycle start. The MCU timestamp is captured
  once per cycle and retained in the payload.
- Sensor fields, payload ordering, and safety thresholds were not changed by
  this timing edit.
- Arduino CLI UNO Q compile passed after the edit. Reported usage: 96,396 bytes
  program storage; 40,984 bytes global variables.
- Physical cadence and worst-case latency remain NOT YET MEASURED. `Bridge.call`
  and peripheral operations may still block.
- Stage 2 remains in progress; watchdog/recovery and hardware validation remain
  pending.
- Files modified: `firmware/mcu/src/main.cpp`, `PROJECT_PROGRESS.md`,
  `DEVELOPMENT_LOG.md`, `NEXT_SESSION.md`, `PHASE_CHECKLIST.md`, and
  `CHANGELOG.md`. No tests or implementation outside this bounded change were
  modified.

## 2026-11-14 — Watchdog deferred; hardware timing blocked

- The user explicitly deferred watchdog implementation until actual timing
  measurements are available and approved a policy of no timeout selection,
  no hardware watchdog enablement, and no automatic watchdog resets.
- The user confirmed the UNO Q 2GB is available and the pending `Wire2` to
  `Wire` change matches actual wiring.
- Arduino CLI `board list` reported **No boards found**. Therefore startup,
  initialization, steady-state loop, worst-case workload, and blocking
  operation maximum durations could not be measured in this environment.
- Recorded the timing measurement procedure and source-known potential blocking
  paths in `firmware/mcu/README.md`. `initializeIMU()` contains a 100 ms delay
  plus synchronous I2C operations; `readIMU()`, serial output, and
  `Bridge.call()` durations/maxima are unmeasured.
- The code contains a clear future watchdog integration point in the MCU build
  notes; no watchdog abstraction or runtime behavior was added. Any future
  watchdog feed must follow successful essential safety work, and the proposed
  timeout/feed policy must be approved before implementation.
- Independence from Linux/Bridge failure is NOT YET VERIFIED. Although local
  safety evaluation runs before `Bridge.call()`, the call's blocking behavior
  and effect on later cycles must be tested on hardware.
- Physical timing values: **NOT YET MEASURED**. No estimates are substituted.
- No firmware was flashed. Watchdog remains unimplemented and disabled.
- Validation after documentation/source work:
  - `.venv\Scripts\python.exe -m pytest` — **111 passed in 0.56s**.
  - `.venv\Scripts\python.exe -m compileall -q ai firmware tests` —
    **passed**.
  - Arduino CLI compile for `arduino:zephyr:unoq` — **passed**; 96,396 bytes
    program storage and 40,984 bytes global variables reported.
  - Arduino CLI `board list` — **No boards found**.
  - `git diff --check` — **passed**.
- No commit or push was made.
- Preserve all uncommitted changes. No commit or push was made.
