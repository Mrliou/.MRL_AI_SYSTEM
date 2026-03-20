# MRL_AI_SYSTEM

FlowAgent / MRL monorepo — compliance + trace + runtime + memory.

## Mother Core Assembly

The system is not a single file — it is a **Mother Core Assembly**: multiple
cores that together satisfy the formula:

```
MotherBody = MaxBoundary + MinPacket + ReversibleChain
```

Design principle: **怎麼過去，就怎麼回來** (the path forward is the path back).

### Six core groups

| # | Name | Role | Entry module |
|---|------|------|--------------|
| 1 | **MotherCore** | Origin signature, canonical law, FluidCore | `00_rootlaw/rootlaw.yaml` |
| 2 | **ParticleReversible** | Compression / expansion / rollback chain | `09_workflow/fltnz_parser.py` |
| 3 | **FlowAgentRuntime** | Persona, memory, language-field, CLI, containers | `04_runtime/flowcore_loop.py` |
| 4 | **WorldModule** | Particle globe, world state, trajectory | `05_persona/world_module.py` |
| 5 | **FileIndexGovernance** | T/X/Y/Z index, librarian, relation chain | `09_workflow/mrl_librarian.py` |
| 6 | **PersonaHistory** | System evolution, alignment, belief stabilisation | `ui/streamlit_app/app.py` |

## Directory structure

| Directory | Layer | Purpose |
|-----------|-------|---------|
| `00_rootlaw/` | L0 ROOT + L3 LAW | Immutable foundational invariants; supersede all other rules |
| `01_schema/` | L1 SEED | JSON Schema contracts for all data flowing through the system |
| `02_principles/` | L3 LAW | AUP-aligned guard rules and default policy settings |
| `03_memory/` | L6 REFLECT | Merkle chain (canonical) + vector store (semantic retrieval) |
| `04_runtime/` | L7 LOOP | FlowAgent kernel — heartbeat loop, trace writer, chain commits |
| `05_persona/` | L4 WORLD | Agent persona definitions, world module, and particle globe |
| `06_trace/` | L6 REFLECT | Dual-stream audit trail: canonical Merkle + operational JSONL |
| `07_ingest/` | L2 PARTICLE | Allowlists, denylists, and ingest source gates |
| `08_sources/` | L0 ROOT | Canonical source manifest (sealed spec mirror) |
| `09_workflow/` | L7 LOOP | Workflow DAGs, orchestration steps, librarian, .fltnz parser |
| `data/` | MetaEnv | Master summaries, module relation chain, librarian index |
| `ui/` | Platform | Streamlit dashboard |

## Key modules

| Module | Purpose |
|--------|---------|
| `09_workflow/mrl_librarian.py` | T/X/Y/Z indexed file librarian — rebuild with `python 09_workflow/mrl_librarian.py index` |
| `09_workflow/fltnz_parser.py` | Bidirectional txt↔fltnz↔map↔flpkg↔trace reversible chain parser |
| `05_persona/world_module.py` | World node / state / trajectory / particle-globe coordinate manager |
| `04_runtime/runtime_manifest.yaml` | TotalCore · Runtime · Container · CLI install & recovery spec |
| `data/relations/module_relations.yaml` | Canonical relation map linking all modules across core groups |
| `03_memory/merkle/memory_chain.py` | Append-only Merkle chain with `verify()` + `rollback()` |
| `09_workflow/api.js` | L0–L7 layer stack (Node.js, v1.3) |
| `09_workflow/signature.js` | LAW-0 signature law implementation |
| `09_workflow/seed.js` | SEED(X) compression pipeline |

## Design principles

- **Deny-by-default** — all external actions blocked unless explicitly allowlisted
- **Audit everything** — every action writes to both Merkle chain and JSONL before execution
- **Human override** — REQUIRE_HUMAN decisions never execute without a recorded proof
- **No hidden instructions** — all directives traceable to a source file in this repo
- **Mutual benefit** — actions must be justified and reversible

## Layer stack (L0–L7)

```
L0 ROOT     source of truth; never deleted
L1 SEED     initial constraints / contracts
L2 PARTICLE content units and state changes
L3 LAW      explicit rules (Rootlaw + compliance + AUP gates)
L4 WORLD    aligned models across worlds
L5 MIRROR   translation of actions/state across worlds
L6 REFLECT  facts, records, accountability
L7 LOOP     validate, then roll forward; rollback with proofs
MetaEnv     variable environment: spawn / scale / snapshot / migrate
Platform    FluinHub / FlowCoreLoop / partner platforms / 3-D globe / AI chat
```

## Quick start

```bash
# 1. Build the librarian index (TXYZ coordinate map)
python 09_workflow/mrl_librarian.py index

# 2. Start the minimal runtime kernel
python 04_runtime/flowcore_loop.py

# 3. Encode a file into the reversible chain
python 09_workflow/fltnz_parser.py encode --src README.md --dst /tmp/readme.fltnz

# 4. Inspect world state
python 05_persona/world_module.py snap
```

See `04_runtime/runtime_manifest.yaml` for the full install order and recovery protocol.
