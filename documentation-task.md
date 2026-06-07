# Repository Documentation Maintenance

## Objective

Maintain a lightweight project knowledge base that accurately reflects the current repository state without introducing process, organizational, or engineering-governance documentation.

Source code is the source of truth.

The repository follows the documentation model:

* `idea.md` = why the project exists
* `architecture.md` = how the system is designed
* `plan.md` = intended future direction
* `project-status.md` = current implementation reality

---

## Documentation Rules

### idea.md

Purpose:

* project vision
* goals
* use cases
* target users
* non-goals

Update only when implementation reveals that the documented project vision is materially incorrect or incomplete.

Do not add implementation details.

---

### architecture.md

Purpose:

* high-level architecture
* service responsibilities
* integrations
* persistence
* communication patterns

Update only when actual architecture differs from documented architecture.

Do not add endpoint inventories, feature lists, or progress tracking.

OpenAPI specifications remain the source of truth for API contracts.

---

### plan.md

Purpose:

* future work
* roadmap
* intended direction

Do not modify roadmap content automatically.

Only report discrepancies between plan and implementation.

---

### project-status.md

Purpose:

Current implementation snapshot.

This is the primary file maintained by autonomous coding sessions.

Update it to reflect:

* implemented functionality
* service inventory
* external integrations
* API surface
* architecture snapshot
* technical debt
* recommendations
* plan vs implementation comparison

---

## Required Analysis

Analyze:

* source code
* repository structure
* configuration
* OpenAPI specifications
* git history
* existing documentation

Identify:

* undocumented functionality
* architecture drift
* implementation progress
* technical debt
* mismatches between plan and implementation

---

## Required Deliverables

1. Update `project-status.md`.

2. Update `architecture.md` only if architecture has changed.

3. Update `idea.md` only if project vision is no longer accurately represented.

4. Do not modify `plan.md`; only report mismatches.

5. If documentation files contain duplicated information, consolidate information into the appropriate target document and remove duplication.

---

## Success Criteria

After execution:

* `idea.md` explains why the project exists.
* `architecture.md` explains how it is designed.
* `plan.md` explains where it intends to go.
* `project-status.md` explains what currently exists.

A future developer should be able to understand the project by reading those four documents before inspecting source code.
