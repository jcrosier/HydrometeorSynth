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

# AD-004: Separation of Geometry and Sampling

**Status:** Accepted

## Decision

Particle classes are deterministic.

They generate exactly the geometry requested by the supplied parameters.

Sampling strategies, parameter distributions, atmospheric parameterisations, random perturbations and orientation models are responsibilities of the dataset generation framework.

## Rationale

This separation:

- keeps particle models simple and deterministic,
- ensures identical inputs always generate identical particles,
- allows multiple dataset generation strategies without modifying particle definitions,
- supports both physically based synthetic datasets and controlled machine learning datasets,
- avoids embedding atmospheric assumptions within particle definitions.

Particle classes define **what** a particle is.

Dataset generation defines **how populations of particles are created**.

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

What is the structure of the 'public API'?

The proposed public API separates the physical particle from its geometric definition.

Example (Bullet Rosette geometry):

particle = Particle(
    geometry=BulletRosette(...),
    dmax=2.3,
    density=917,
)

Status: Under discussion.

---

## AQ-003

Should Particle instances be mutable?

Current discussion:

- Geometry should remain fixed after construction.
- Physical properties such as orientation and Dmax may be mutable for efficient experimentation.
- This will be evaluated during implementation of the first Particle API.

---