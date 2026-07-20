# Architectural Decisions

This document records significant architectural decisions made during the early development of HydrometeorSynth.

As the project matures, these decisions will be migrated into individual Architecture Decision Records (ADRs).

---

# AD-001: Separation of Geometry and Physical State

**Status:** Accepted

## Decision

HydrometeorSynth separates canonical particle geometry from physical particle state.

A `Geometry` object defines only the particle's shape, but includes a canonical size (canonical `Dmax`).

A `Particle` combines a `Geometry` with physical properties including:

- maximum dimension (`Dmax`),
- density,
- orientation.

All higher-level workflows operate on `Particle` objects.

## Rationale

Separating shape from physical state:

- keeps geometry implementations independent of physical units,
- allows the same geometry model to represent particles of different sizes,
- simplifies procedural geometry generation,
- keeps physical properties independent from geometric modelling.

`Geometry` answers the question:

> *"What shape is this?"*

`Particle` answers the question:

> *"What physical object is this?"*

---

# AD-002: Streaming Processing

**Status:** Accepted

## Decision

HydrometeorSynth adopts a streaming processing model.

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
- `particle`
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

Geometry classes are deterministic.

They generate exactly the geometry requested by the supplied parameters.

Sampling strategies, parameter distributions, atmospheric parameterisations, random perturbations and orientation models are responsibilities of the dataset generation framework.

## Rationale

This separation:

- keeps geometry models simple and deterministic,
- ensures identical inputs always generate identical geometry,
- allows multiple dataset generation strategies without modifying geometry implementations,
- supports both physically based synthetic datasets and controlled machine learning datasets,
- avoids embedding atmospheric assumptions within geometry definitions.

Geometry defines **what shape** a particle has.

Dataset generation defines **how particle populations are created**.

---

# AD-005: Geometry Abstraction

**Status:** Accepted

## Decision

Each `Particle` owns a `Geometry` object.

`Geometry` implementations provide a common interface regardless of the underlying representation (procedural geometry, imported meshes, or future implementations).

`Geometry` is responsible for:

- defining parameters,
- parameter validation,
- mesh generation,
- canonical geometric properties,
- cache management.

## Rationale

Separating geometry behind a common interface allows new geometry implementations without affecting the remainder of the system.

Keeping geometric responsibilities within `Geometry` maintains a clear separation between modelling shape and representing physical particles.

---

# AD-006: Thin Particle

**Status:** Accepted

## Decision

`Particle` is intentionally a lightweight domain object.

It owns:

- geometry,
- Dmax,
- density,
- orientation.

It derives physical properties such as volume, surface area and mass from these values.

`Particle` does not perform:

- geometry generation,
- random sampling,
- rendering,
- imaging,
- dataset generation.

## Rationale

A particle represents a single physical object.

Keeping the class lightweight produces a simple, intuitive API while allowing other components to evolve independently.

---

# AD-007: Mutable Geometry

**Status:** Accepted

## Decision

Geometry objects are mutable.

Changing a defining parameter automatically invalidates cached derived state.

Derived quantities are recomputed lazily when next requested.

`Particle` performs no cache management.

## Rationale

Interactive scientific workflows frequently involve modifying geometric parameters while exploring particle morphology.

Automatic cache invalidation provides a simple programming model while avoiding unnecessary recomputation.

---

# AD-008: Canonical Geometry

**Status:** Accepted

## Decision

Geometry is represented in canonical coordinates independent of physical scale.

Physical size is applied by the owning `Particle` through its `Dmax`.

## Rationale

This approach:

- separates shape from scale,
- simplifies geometry implementations,
- centralises scaling logic,
- avoids embedding physical units within procedural geometry.

---

# AD-009: Geometry Caching

**Status:** Accepted

## Decision

Only `Geometry` caches derived computations.

Cached quantities include:

- mesh,
- canonical volume,
- canonical surface area.

`Particle` derives physical properties directly from the geometry and performs no caching.

## Rationale

Geometry operations such as mesh generation are computationally expensive and benefit from caching.

Particle calculations are inexpensive arithmetic and do not justify additional cache complexity.