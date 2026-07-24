# Architectural Decisions

This document records significant architectural decisions made during the early development of HydrometeorSynth.

As the project matures, these decisions will be migrated into individual Architecture Decision Records (ADRs).

---

# AD-001: Separation of Geometry and Physical State

**Status:** Accepted

## Decision

HydrometeorSynth separates canonical particle geometry from physical particle state.

A `Geometry` object defines only the particle's shape, but includes a canonical size (canonical `Dmax`).

A `Position` object defines only the particle's location in space.

A `Orientation` object defines only the particle's orientation in space.

A `Particle` combines `Geometry`, `Orientation` and `Position` which provides physical properties including:

- maximum dimension (`Dmax`),
- density,
- location,
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

`Orientation` answers the question:

> *"How is this orientated?"*

`Position` answers the question:

> *"Where is this located?"*

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

Packages are organised according to their primary responsibilities while maintaining a layered architecture and clear separation of concerns.

The structure intentionally separates:

- domain modelling (`geometry`, `particle`),
- image generation (`imaging`),
- application workflows (`datasets`, `viewer`),
- persistence (`io`).

The package structure is intentionally small and should only expand when justified by new functionality.

---

# AD-004: Separation of Geometry, Orientation, Position and Sampling

**Status:** Accepted

## Decision

Geometry, Orientation, and Position classes are deterministic.

They generate exactly the geometry requested by the supplied parameters.

Sampling strategies, parameter distributions, atmospheric parameterisations, random perturbations and orientation models are responsibilities of the dataset generation framework.

## Rationale

This separation:

- keeps component models simple and deterministic,
- ensures identical inputs always generate identical output,
- allows multiple dataset generation strategies without modifying implementations,
- supports both physically based synthetic datasets and controlled machine learning datasets,
- avoids embedding atmospheric assumptions within geometry definitions.

Geometry defines **what shape** a particle has.

Orientation defines **what orientation** a particle has.

Position defines **where** a particle is.

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
- position

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

---

# AD-010: Mutable Particles

**Status:** Accepted

## Decision 

Particle objects are mutable.

Changing a defining parameter automatically invalidates cached derived state.

Derived quantities are recomputed lazily when next requested.

Property setters are responsible for validating inputs and maintaining object consistency.

## Rationale

The Particle class shall be mutable to support interactive scientific exploration. Physical properties such as dmax, density, and orientation may be modified after construction. 

---

# AD-011: Orientation API

**Status:** Accepted

## Decision

`Orientation` represents the rotational state of a particle using rotations about the x, y, and z axes.. It shall accept three named Euler angles in **degrees**, with the following valid ranges:

- 0 ≤ x_rotation < 360
- 0 ≤ y_rotation < 360
- 0 ≤ z_rotation < 360

Values outside this range are considered invalid and shall raise a ValueError.

Floating-point values are permitted.

`Orientation` is mutable to allow interactive control and experimentation.

## Rationale

Particles require an orientation to support imaging and rendering. Several public APIs were considered, including positional arguments, tuples of angles, and named parameters.

The public API should be explicit, readable and self-documenting, following the design principles already established for the Particle domain object.

---

# AD-012 — Position Domain Object

**Status:** Accepted

## Decision

Position represents the location of a particle in a three-dimensional coordinate system. It is a mutable value object containing validated x, y, and z components. Position is independent of Geometry, Particle, and imaging. Coordinates must be finite real numbers and are not range-limited.

---

# AD-013: Imaging Subsystem

**Status:** Accepted

## Decision

The imaging subsystem separates the description of viewing geometry, rendering, and rendered output into distinct classes.

The initial imaging architecture consists of:

- `Camera`
- `Renderer`
- `Image`

`Camera` describes the viewing geometry, including:

- position,
- orientation,
- pixel size,
- width,
- height.

`Renderer` converts a `Particle` into an `Image` using a specified `Camera`.

`Image` represents the rendered image and owns the image pixel buffer. It is independent of the rendering process and may be reused across multiple rendering operations.

## Rationale

Separating these responsibilities keeps the imaging subsystem modular, reusable and extensible.

`Camera` describes **how** a scene is viewed, but performs no rendering.

`Renderer` performs the computational work of projecting particles into image space. It owns neither particle state nor camera state.

`Image` represents the rendering result independently of the rendering process.

This separation allows new camera models, rendering implementations and sensor response models to be introduced without changing the particle domain model.

---

# AD-014: Mutable Camera

**Status:** Accepted

## Decision

`Camera` objects are mutable.

Camera properties are modified through validated property setters.

These include:

- position,
- orientation,
- pixel size,
- width,
- height.

All camera properties shall maintain a valid state through property validation.

## Rationale

A mutable camera simplifies interactive applications such as viewers and graphical user interfaces, where camera properties are frequently adjusted by the user.

This approach is consistent with the existing mutable domain objects (`Geometry`, `Particle`, `Orientation`, and `Position`) and provides a uniform programming model throughout the project.

Validation performed by property setters ensures that camera objects always remain in a valid state.

---

# AD-015: Fixed Camera Configuration for Dataset Generation

**Status:** Accepted

## Context

HydrometeorSynth supports multiple workflows that utilise the imaging subsystem. Two primary workflows have been identified:

- **Dataset generation**, where large numbers of particles are rendered in a streaming pipeline and written to a Zarr dataset.
- **Interactive viewing**, where users can manipulate the camera configuration to inspect individual particles.

During dataset generation, all rendered particles should be produced under a consistent imaging configuration to ensure scientific reproducibility and to simplify the resulting dataset structure.

## Decision

A dataset generation job shall use a fixed camera configuration for its entire lifetime.

All particles within a dataset shall be rendered using the same camera definitions. Camera properties, including projection, position, orientation, pixel size, image dimensions and any future rendering parameters, shall remain constant throughout dataset generation.

Camera metadata shall therefore be stored once as dataset-level metadata rather than duplicated for every particle.

The `Camera` class shall remain mutable to support interactive applications. However, the dataset generation API shall enforce that camera configurations remain fixed for the duration of a dataset generation job.

## Consequences

### Positive

- Produces scientifically consistent datasets.
- Simplifies the dataset data model.
- Eliminates duplication of camera metadata.
- Improves storage efficiency.
- Ensures reproducible rendering conditions.
- Separates the concerns of dataset generation and interactive viewing.
- Allows the same mutable `Camera` implementation to be reused by both workflows.

### Negative

- A single dataset cannot represent particles rendered using varying camera configurations.
- Experiments requiring varying camera geometry must be represented using separate dataset generation workflows or dataset formats.

## Alternatives Considered

### Store camera metadata per particle

This would permit camera properties to vary between particles but would significantly increase metadata duplication, complicate the dataset structure and reduce the semantic consistency of datasets intended for machine learning.

### Make `Camera` immutable

An immutable camera would naturally enforce fixed dataset generation but would unnecessarily restrict interactive viewers and graphical applications where camera parameters are expected to change dynamically.

This alternative was rejected because mutability is appropriate for the `Camera` domain object, while enforcement of fixed camera configurations is the responsibility of the dataset generation API.