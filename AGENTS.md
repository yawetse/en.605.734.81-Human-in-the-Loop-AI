# Repository Instructions

## LID

- Mode: Scoped
- Version: 1.2.0

## LID Scope

Paths in scope:

- `module_03/mod_03_assignment/**`
- `docs/high-level-design.md`
- `docs/intent/cloud-kitchen-simulation/**`

Paths explicitly excluded:

- None.

## Linked-Intent Development (MANDATORY)

**Consult the `linked-intent-dev` skill for ALL code changes within the declared scope.** All changes flow through the arrow of intent in one direction:

```
HLD -> LLDs -> EARS -> Tests -> Code
```

- **New features and refactors**: use the full six-phase workflow: HLD check, LLD check or draft, EARS, intent-narrowing edge audit, tests first, and code.
- **Bug fixes**: walk the arrow like any other change. Find where behavior diverged from intent and cascade from there.
- **If unsure**: use the full workflow.

Stop after each phase for user review. Docs carry current intent and must be readable without conversation history. Preserve current rationale, alternatives, and constraints, but remove discussion residue. Record rejected alternatives and their rationale in the owning LLD's Decisions and Alternatives table.

**Memory vs. intent.** Project intent belongs in the arrow so that it travels across tools and sessions. User preferences and personal working style belong in memory.

### Navigation

| What you need | Where to look |
| --- | --- |
| High-level design | `docs/high-level-design.md` |
| Design tree | `docs/intent/`, with one folder per node |
| EARS specs | Beside each design doc as `{node}-specs.md` |
| Decision docs | `docs/decisions/` for project decisions and `docs/intent/<segment>/decisions/` for segment decisions |

### Terminology

- **HLD**: The project-level high-level design at `docs/high-level-design.md`.
- **LLD**: A detailed component design under `docs/intent/`. Leaf LLDs own EARS requirements.
- **EARS**: Structured one-line requirements stored beside the owning LLD. Markers are `[x]` implemented, `[ ]` active gap, and `[D]` deferred.
- **Arrow**: The one-way chain from HLD to LLDs to EARS to tests to code.
- **Arrow segment**: One leaf LLD plus the specs, tests, and code that cite its EARS prefix.
- **Cascade**: Propagating an intent change through downstream levels so adjacent artifacts remain coherent.

### Code annotations

Annotate code and tests with `@spec` comments citing the owning EARS IDs:

```python
# @spec CKS-FUL-001
```

Place an annotation on the entry point that owns the specified behavior. Tests cite the specification directly exercised by the test.
