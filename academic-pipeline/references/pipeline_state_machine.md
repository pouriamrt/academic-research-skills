# Pipeline State Machine v2.0 — Complete Definition

This document defines all legal states, transition conditions, transition actions, and exception handling for academic-pipeline v2.0.

---

## State Definitions

### Stage States

| State | Description |
|-------|------------|
| `pending` | Not yet started, waiting for prerequisite stage to complete |
| `in_progress` | Currently executing |
| `completed` | Completed, deliverables recorded |
| `skipped` | User chose to skip (only for non-mandatory stages) |
| `blocked` | Preconditions not met (e.g., integrity check FAIL) |

### Pipeline Global States

| State | Description |
|-------|------------|
| `initializing` | Detecting entry point and materials |
| `running` | Pipeline executing (at least one stage is in_progress) |
| `awaiting_confirmation` | Stage complete, waiting for user to confirm checkpoint |
| `paused` | User paused, can resume at any time |
| `completed` | All required stages complete, final paper produced |
| `aborted` | User abandoned (e.g., chose to abandon after Reject) |

---

## State Transition Diagram (ASCII)

```
                        +-------------+
                        | INITIALIZING|
                        +------+------+
                               |
                    [Detect entry point & materials]
                               |
         +----------+----------+----------+----------+
         |          |          |          |          |
         v          v          v          v          v
    +--------+ +--------+ +--------+ +--------+ +--------+
    |Stage 1 | |Stage 2 | |Stg 2.5 | |Stage 3 | |Stage 4 |
    |RESEARCH| | WRITE  | |INTEGRIT| | REVIEW | | REVISE |
    +---+----+ +---+----+ +---+----+ +---+----+ +---+----+
        |          |          |          |          |
   [checkpoint]   [checkpoint]   |     [checkpoint]  |
        |          |          |          |          |
        v          |          v          v          v
   [Detect        |     +---+----+    |          |
    routing       |     |PASS?   |    |          |
    flags]        |     +---+----+    |          |
        |         |         |         |          |
   +----+----+    |    +----+----+    |          |
   |         |    |    |         |    |          |
  EXP     No EXP  |   Yes       No    |          |
  needed  needed  |    |     [Fix]    |          |
   |         |    |    |   [Re-verify]|          |
   v         |    |    |        |     |          |
+--------+   |    |  [checkpoint]|    |          |
|Stg 1.5 |   |    |    |        |    |          |
|EXPERIM.|   |    |    v        |    |          |
+---+----+   |    |  +--------+ |    |          |
    |        |    |  |Stage 3 |<+    |          |
 [1.5a DESIGN]   |  | REVIEW |      |          |
    |        |    |  +---+----+      |          |
 [1.5b EXECUTE]  |      |           |          |
    |        |    |  [DECISION]      |          |
 [1.5c LOG]  |    |      |          |          |
    |        |    |      |          |          |
 [checkpoint]|    +---------+---------+     |          |
    |        |    |         |         |     |          |
    +---+----+  Accept    Minor     Major   |          |
        |         |       Revision  Revision|          |
        v         |         |         |     |          |
   +--------+     |    [checkpoint]  [checkpoint]      |
   |Stage 2 |     |         |         |     |          |
   | WRITE  |     |         v         v     |          |
   +---+----+     |    +--------+ +--------+|          |
        |         |    |Stage 4 | |Stage 4 ||          |
   [checkpoint]   |    | REVISE | | REVISE ||          |
        |         |    +---+----+ +---+----+|          |
        v         |        |          |     |          |
   +--------+     |   [checkpoint]   [checkpoint]      |
   |Stg 2.5 |    |        |          |     |          |
   |INTEGRIT|    |        v          v     |          |
   +---+----+    |    +--------+ +--------+           |
        |         |    |Stg 3'  | |Stg 3'  |           |
        |         |    |RE-REV. | |RE-REV. |           |
        v         |    +---+----+ +---+----+           |
   +---+----+     |        |          |                 |
   |PASS?   |     |   [DECISION]  [DECISION]            |
   +---+----+     |        |          |                 |
        |         |     Accept      Major               |
   +----+----+    |     /Minor        |                 |
   |         |    |        |     [checkpoint]           |
  Yes       No    |        |          |                 |
   |     [Fix]    |        |          v                 |
   |   [Re-verify]|        |     +--------+             |
[checkpoint]  |    |        |     |Stg 4'  |             |
   |         |    |        |     |RE-REVIS|             |
   v         |    |        |     +---+----+             |
+--------+   |    |        |          |                 |
|Stage 3 |<--+    |   [checkpoint]  [checkpoint]        |
| REVIEW |         |        |          |                 |
+---+----+         v        v          v                 |
                +----+--------+----------+-----+           |
                |     Stage 4.5                |           |
                |   FINAL INTEGRITY            |           |
                +----------+------------------+           |
                           |                               |
                      [PASS? Zero issues]                  |
                           |                               |
                     +-----+-----+                         |
                     |           |                         |
                    Yes         No                         |
                     |        [Fix]                         |
                     |      [Re-verify]                     |
                [checkpoint]     |                         |
                     |           |                         |
                     v           |                         |
                +--------+       |                         |
                |Stage 5 | <-----+                         |
                |FINALIZE|                                 |
                +---+----+                                 |
                    |                                      |
               [checkpoint]                                |
                    |                                      |
                    v                                      |
                +--------+                                 |
                |Stage 6 |                                 |
                |PROCESS |                                 |
                |SUMMARY |                                 |
                +---+----+                                 |
                    |                                      |
                    v                                      |
                +-------+                                  |
                |  END  |                                  |
                +-------+                                  |
```

---

## Legal State Transitions

### Normal Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| INIT | Stage 1 | User confirms starting from Stage 1 | Detect mode preference, launch deep-research |
| INIT | Stage 2 | User has research materials, confirms skipping Stage 1 | Detect materials, launch academic-paper |
| INIT | Stage 2.5 | User has complete paper | Launch integrity_verification_agent |
| INIT | Stage 3 | User has verified paper + integrity report | Confirm paper language/domain, launch reviewer |
| INIT | Stage 4 | User has review comments | Confirm paper + review comments, launch revision |
| INIT | Stage 5 | User has final draft for format conversion | Confirm format requirements, launch format-convert |
| Stage 1 | **checkpoint (post-1)** | Stage 1 completed | Wait for user confirmation; detect routing flags |
| checkpoint (post-1) | Stage 1.5a | User confirms + Methodology Blueprint has `requires_experiment_design=true` OR `requires_simulation=true` | Create lab notebook, launch experiment-designer |
| checkpoint (post-1) | Stage 2 | User confirms + no experiment routing flags | handoff RQ Brief + Bibliography + Synthesis |
| Stage 1.5a | **checkpoint (post-1.5a)** | Stage 1.5a completed, Schema 10 produced | Wait for user confirmation |
| checkpoint (post-1.5a) | Stage 1.5b | User confirms | Pass Schema 10 (+ Schema 13 if simulation) to data-analyst or simulation-runner |
| Stage 1.5b | **checkpoint (post-1.5b)** | Stage 1.5b completed, Schema 11 produced | Wait for user confirmation |
| checkpoint (post-1.5b) | Stage 1.5c | User confirms | Pass notebook to lab-notebook export mode |
| Stage 1.5c | **checkpoint (post-1.5c)** | Stage 1.5c completed, Schema 12 produced | Wait for user confirmation |
| checkpoint (post-1.5c) | Stage 2 | User confirms | handoff RQ Brief + Bibliography + Synthesis + Schema 10 + Schema 11 + Schema 12 |
| Stage 2 | **checkpoint** | Stage 2 completed, Paper Draft produced | Wait for user confirmation |
| checkpoint | Stage 2.5 | User confirms | Pass Paper Draft to integrity agent |
| Stage 2.5 | **checkpoint** | PASS | Wait for user confirmation |
| Stage 2.5 | Stage 2.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint | Stage 3 | User confirms | Pass verified paper to reviewer |
| Stage 3 | **checkpoint** | Decision produced | Wait for user confirmation |
| checkpoint | **Experiment Re-Entry Check** | Decision = Minor/Major, user confirms | Scan Revision Roadmap for `requires_new_experiment` items |
| Experiment Re-Entry Check | Stage 1.5-R | Experiment items found AND user confirms re-entry | Dispatch experiment sub-stages based on experiment_type |
| Experiment Re-Entry Check | Stage 4 | No experiment items OR user opts out | Pass Revision Roadmap to revision coaching |
| Stage 1.5-R | Stage 4 | New Schema 11 produced | Merge new results with existing materials; pass to revision coaching |
| checkpoint | Stage 4.5 | Decision = Accept, user confirms | Skip revision, go directly to final verification |
| Stage 4 | **checkpoint** | Stage 4 completed | Wait for user confirmation |
| checkpoint | Stage 3' | User confirms | Pass Revised Draft + Response to Reviewers |
| Stage 3' | **checkpoint** | Decision produced | Wait for user confirmation |
| checkpoint | Stage 4.5 | Decision = Accept/Minor, user confirms | Pass final draft to final verification |
| checkpoint | Stage 4' | Decision = Major, user confirms | Pass new Revision Roadmap |
| Stage 4' | **checkpoint** | Stage 4' completed | Wait for user confirmation |
| checkpoint | Stage 4.5 | User confirms | Pass revised draft to final verification |
| Stage 4.5 | **checkpoint** | PASS (zero issues) | Wait for user confirmation |
| Stage 4.5 | Stage 4.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint | Stage 5 | User confirms | Pass final accepted draft |
| Stage 5 | **checkpoint (post-5)** | Stage 5 completed, final paper produced | Wait for user confirmation |
| checkpoint (post-5) | Stage 6 | User confirms | Launch process summary generation |
| Stage 6 | END | Stage 6 completed, process record PDF produced | Pipeline complete |

### Special Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| Stage 3 (Reject) | Stage 2 | User chooses to restructure | Clear Stage 2-3 state, preserve Stage 1 materials, restart Stage 2 |
| Stage 3 (Reject) | ABORT | User chooses to abandon | Save all produced materials, mark pipeline aborted |
| Stage 3' (Major) | Stage 4' | User confirms | Last revision opportunity |
| Stage 4' | Stage 4.5 | Revision complete | Go directly to final verification (no return to review) |
| Any stage | PAUSED | User says "pause" or "stop here" | Save pipeline state |
| PAUSED | Previous stage | User returns to continue | Restore pipeline state, display Dashboard |

### Experiment Re-Entry Transitions (NEW in v2.8)

| From | To | Precondition | Action |
|------|----|-------------|--------|
| Stage 3 (Minor/Major) | **Stage 1.5-R** | Revision Roadmap contains item(s) with `requires_new_experiment = true` AND user confirms experiment re-entry | Dispatch experiment sub-stages based on `experiment_type`; preserve all Stage 1-3 materials |
| **Stage 1.5-R** | Stage 4 | Stage 1.5-R produces new Schema 11 | Merge new experiment results with existing materials; proceed to revision coaching then Stage 4 |
| Stage 3' (Major) | **Stage 1.5-R2** | New Revision Roadmap contains item(s) with `requires_new_experiment = true` AND user confirms | Dispatch experiment sub-stages; this is the LAST experiment opportunity |
| **Stage 1.5-R2** | Stage 4' | Stage 1.5-R2 produces new Schema 11 | Merge new experiment results; proceed to residual coaching then Stage 4' |

**Stage 1.5-R sub-stages follow the same protocol as Stage 1.5 (design -> execute -> log), but may skip the design phase when `experiment_type = "additional_analysis"` (re-use existing Schema 10).**

**User opt-out**: At each experiment re-entry checkpoint, the user may choose to skip experiments and mark those items as "Acknowledged Limitations" instead. This is a valid academic choice (not all reviewer requests must be fulfilled).

### Prohibited Transitions (Illegal)

| From | To | Reason |
|------|----|--------|
| Stage 1 | Stage 2 (when routing flags require experiment) | Cannot skip Stage 1.5 when `requires_experiment_design=true` or `requires_simulation=true` |
| Stage 1.5a | Stage 2 | Cannot skip Stage 1.5b execution (design must be executed) |
| Stage 1.5b | Stage 2 | Cannot skip Stage 1.5c export (lab record must be produced) |
| Stage 1 | Stage 3 | Cannot skip Stage 2 and 2.5 (unless mid-entry + has paper) |
| Stage 2 | Stage 3 | **Cannot skip Stage 2.5 (integrity check is mandatory)** |
| Stage 4 | Stage 5 | Cannot skip RE-REVIEW (revision must be re-reviewed) |
| Stage 3' | Stage 5 | **Cannot skip Stage 4.5 (final integrity check is mandatory)** |
| Stage 4' | Stage 3' | Cannot return to RE-REVIEW (max 1 round of RE-REVISE) |
| Stage 5 | Stage 3 | Cannot roll back (no review after FINALIZE) |
| completed | in_progress | Completed stages cannot restart |

---

## Material Dependency Matrix

| Material | Produced At | Consumed At | Required/Recommended |
|----------|-----------|-------------|---------------------|
| RQ Brief | Stage 1 | Stage 1.5a (input), Stage 2 (Phase 0) | Recommended |
| Methodology Blueprint | Stage 1 | Stage 1 checkpoint (routing flags), Stage 1.5a (input), Stage 2 (Phase 0) | Recommended |
| Bibliography | Stage 1 | Stage 2 (Phase 1) | Recommended |
| Synthesis Report | Stage 1 | Stage 2 (Phase 3) | Recommended |
| **Experiment Design (Schema 10)** | **Stage 1.5a** | **Stage 1.5b (input), Stage 2 (Methods)** | **Required if Stage 1.5 active** |
| **Simulation Spec (Schema 13)** | **Stage 1.5a** | **Stage 1.5b (input, simulation-runner only)** | **Required if `requires_simulation=true`** |
| **Experiment Results (Schema 11)** | **Stage 1.5b** | **Stage 2 (Results section)** | **Required if Stage 1.5 active** |
| **Lab Record (Schema 12)** | **Stage 1.5c** | **Stage 2 (Methods section)** | **Required if Stage 1.5 active** |
| **Revision Experiment Results (Schema 11-R)** | **Stage 1.5-R** | **Stage 4 (Results integration)** | **Required if Stage 1.5-R active** |
| **Revision Lab Record (Schema 12-R)** | **Stage 1.5-R** | **Stage 4 (Methods integration)** | **Required if Stage 1.5-R active** |
| Paper Draft | Stage 2 | Stage 2.5 (input) | **Required** |
| **Integrity Report (Pre)** | **Stage 2.5** | **Stage 3 (prerequisite)** | **Required** |
| **Verified Paper Draft** | **Stage 2.5** | **Stage 3 (Phase 0)** | **Required** |
| Review Reports (x5) | Stage 3 | Stage 4 (input) | Required |
| Editorial Decision | Stage 3 | Stage 4 (input) | Required |
| Revision Roadmap | Stage 3 | Stage 4 (input) | Required |
| Revised Draft | Stage 4 | Stage 3' (Phase 0) | Required |
| Response to Reviewers | Stage 4 | Stage 3' (input) | Recommended |
| **Re-Review Report** | **Stage 3'** | **Stage 4' (input)** | **Required (if Major)** |
| **Re-Revised Draft** | **Stage 4'** | **Stage 4.5 (input)** | **Required (if executed)** |
| **Integrity Report (Final)** | **Stage 4.5** | **Stage 5 (prerequisite)** | **Required** |
| Final Paper | Stage 5 | Stage 6 (input) | Required |
| **Process Record** | **Stage 6** | **END (delivery)** | **Required** |

---

## Exception State Handling

### Timeout

If a stage shows no progress for an extended period (e.g., Socratic mode exceeds 15 rounds without convergence):
1. state_tracker marks the stage as `stalled`
2. orchestrator provides options:
   - Switch mode (socratic -> full)
   - Narrow scope
   - Skip this stage (non-mandatory stages only)

### Missing Materials

If required materials are found missing during transition:
1. state_tracker reports the material gap
2. orchestrator suggests returning to the stage that produces that material
3. User can choose: backfill / skip (at own risk, but cannot skip integrity checks)

### Integrity Check FAIL Loop

If Stage 2.5 or 4.5 corrections exceed 3 rounds without passing:
1. List all unverifiable items
2. User decides:
   - Manually handle unverifiable items
   - Remove unverifiable citations
   - Continue to next stage (with "partially unverified" warning)

### Session Interruption

If the user leaves and returns:
1. orchestrator displays Progress Dashboard
2. Confirm whether to continue from breakpoint
3. Check if any outdated materials need refreshing

---

## Revision Loop Rules (v2.0)

### Simplified Revision Cycle

```
v2.0's revision cycle is simpler and more explicit than v1.0:

Stage 3 (First REVIEW)
  -> Decision: Accept -> Stage 4.5
  -> Decision: Minor/Major -> Stage 4
      -> Stage 4 (REVISE)
          -> Stage 3' (RE-REVIEW, verification)
              -> Decision: Accept/Minor -> Stage 4.5
              -> Decision: Major -> Stage 4' (last revision)
                  -> Stage 4.5 (go directly to final verification, no return to review)

Maximum 1 round of RE-REVISE, no infinite loops.
Unresolved issues -> Acknowledged Limitations.
```

### Differences from v1.0

| v1.0 | v2.0 |
|------|------|
| Max 2 review-revise cycles | Fixed 2 reviews (Stage 3 + Stage 3') + max 1 RE-REVISE |
| No integrity check | Mandatory Pre-review + Final integrity check |
| 4 reviewers | 5 reviewers (+Devil's Advocate) |
| Can skip any stage | Stage 2.5 and 4.5 cannot be skipped |
| No mandatory checkpoints | Every stage requires a checkpoint |
