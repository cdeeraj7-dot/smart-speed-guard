# Smart Speed Guard — Project Progress

Last verified checkpoint: 2026-11-14 (IST)

## Current phase

Stage 2 — MCU foundation (IN PROGRESS). Stage 0's repository inventory
reconciliation and Stage 1's repository/build setup are complete. The MCU loop
now uses elapsed-time scheduling instead of a fixed 500 ms delay. Hardware
startup/loop timing, watchdog/recovery, and safety behavior remain unverified.
Watchdog configuration is **PENDING TIMING MEASUREMENTS** and explicitly
deferred by the user. No timeout or feed policy is selected.

Actual startup, initialization, steady-state loop, worst-case loop, and
blocking-operation maximum durations: **NOT YET MEASURED**. Arduino CLI found
no attached board during this checkpoint. Linux/Bridge failure independence is
also **NOT YET VERIFIED**.

The current engineering work is at an early MCU/sensor and telemetry bring-up
stage. It is not a completed hardware integration phase.

## Completed phases and verified outcomes

- Stage 0 architecture audit: repository inventory reconciled to the current
  source tree; technical board/electrical/protocol decisions remain unresolved.
- Stage 1 repository/build setup: Arduino CLI sketch entry and build
  instructions added; compile succeeded for `arduino:zephyr:unoq` with core
  1.0.0, CLI 1.5.1, and RouterBridge 0.4.3.
- Python test suite: 111 passed on 2026-11-14.
- Python syntax check (`compileall` for `ai`, `firmware`, and `tests`) passed on
  2026-11-14.
- Latest verification: Python suite 111 passed in 0.56s; compileall passed;
  UNO Q CLI cross-compile passed (96,396 bytes program, 40,984 bytes globals).
- No implementation phase has been accepted as fully complete based on these
  checks alone.

## Pending phases

See [PHASE_CHECKLIST.md](./PHASE_CHECKLIST.md) for all 21 development stages,
tasks, acceptance criteria, test status, and approval dependencies.

Current gates include:

- Verify board/toolchain/domain interfaces from authoritative sources.
- Measure actual startup, initialization, loop and blocking-operation durations
  on attached UNO Q hardware under normal and failure workloads.
- Establish that Linux/Bridge failure cannot starve MCU safety operation.
- Keep watchdog disabled until timing results are recorded and the proposed
  timeout/feed policy is approved.
- Establish and test sensor interfaces with verified electrical details.
- Specify, test, and physically verify the full MCU/Linux message contract.
- Complete hardware, offline/recovery, and end-to-end testing.
- Do not infer sensor readings for sensors whose acquisition is not implemented.

## Current priorities

1. Obtain actual MCU timing measurements; watchdog configuration is PENDING
   TIMING MEASUREMENTS and requires user approval after a proposal.
2. Preserve all pre-existing uncommitted source changes; do not commit or push.
3. Keep electrical, transport, and hardware claims marked unverified
   until supported by authoritative sources or tests.
4. Arrange controlled hardware checks for sensor reads, timing, and Bridge
   failure behavior.

## Deadline status

The supplied deadline is 2026-11-15 23:59 IST. At this checkpoint (2026-11-14),
it is approaching. The offline Python suite and UNO Q cross-compile passed; no
board was attached for timing or Bridge measurements. Physical verification,
timing measurements, and Monday integration preparation remain outstanding.
No claim is made that the deadline handover is complete.

## Working-tree checkpoint

Current tracked modifications include:

- `docs/architecture/ARCHITECTURE_AUDIT.md`
- `firmware/linux/README.md`
- `firmware/linux/receiver.py`
- `firmware/mcu/include/telemetry.h`
- `firmware/mcu/src/imu.cpp`
- `firmware/mcu/src/main.cpp`
- `firmware/mcu/src/telemetry.cpp`

The modifications to `firmware/mcu/src/imu.cpp` were present in the worktree;
inspection shows the uncommitted edit changes I2C calls from `Wire2` to `Wire`.
The user confirmed the change is intentional and matches actual wiring.
Hardware read behavior remains untested.

New files include the five root checkpoint documents, `firmware/mcu/mcu.ino`,
and `firmware/mcu/README.md`. The latest code operation was a successful
cross-compile; no firmware was flashed. No commit or push was made.

No commit or push was made for this checkpoint.
