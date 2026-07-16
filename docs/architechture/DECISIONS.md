# Architectural Decisions

This document records significant architectural decisions made during the early development of HydrometeorSynth.

As the project matures, these decisions will be migrated into individual Architecture Decision Records (ADRs).

---

# AD-001: Particle-Centric Architecture

**Status:** Accepted

## Decision

The `Particle` is the central domain object within HydrometeorSynth.

All major workflows operate on particles rather than directly on meshes, images or datasets.

## Rationale

HydrometeorSynth is fundamentally a particle modelling framework.

Geometry generation, imaging, metadata generation and dataset creation are all operations performed on particles.

Using the particle as the central abstraction results in an API that reflects the scientific domain and remains intuitive for users.

---

# AD-002: Streaming Processing

**Status:** Accepted

## Decision

HydrometeorSynth shall adopt a streaming processing model.

Particles are generated, processed, written to disk and discarded without retaining large collections of particle meshes in memory.

## Rationale

Typical dataset generation may involve millions of particles.

Streaming processing:

- minimises memory usage,
- simplifies execution,
- naturally supports parallel processing,
- avoids unnecessary object lifetime management.

---

# AD-003: Package Structure

**Status:** Accepted

## Decision

The initial top-level package structure is:

- `geometry`
- `particles`
- `imaging`
- `datasets`
- `io`
- `viewer`

## Rationale

Packages are organised according to user-facing responsibilities while maintaining clear separation of concerns.

The structure is intentionally small and should only expand when justified by new functionality.

---

# Open Architectural Questions

The following topics remain under discussion.

## AQ-001

How should particle geometry be represented internally?

Current leading proposal:

- A `Particle` owns a `Geometry` object.
- Different geometry implementations (procedural, imported mesh) provide a common interface.

Status: Under discussion.

---

## AQ-002

What constitutes the minimal public interface of a `Particle`?

Status: Under discussion.