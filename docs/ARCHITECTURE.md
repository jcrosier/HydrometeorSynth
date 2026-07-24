# Architecture

**Project:** HydrometeorSynth

**Version:** Draft 0.2

---

# Purpose

This document describes the high-level software architecture of HydrometeorSynth.

It defines the major software components, their responsibilities and interactions. Implementation details, algorithms and individual class designs are documented separately as the project evolves.

The rationale for significant architectural decisions is recorded in the project's Architecture Decision Records (ADRs).

---

# High-Level Architecture

HydrometeorSynth is organised into a small number of high-level components, each with a clearly defined responsibility.

| Component | Responsibility |
|-----------|----------------|
| `geometry` | Canonical geometric representations, mesh generation, geometric calculations and transformations. |
| `particle` | Physical particle representation combining geometry with physical properties. |
| `imaging` | Camera models, image representation, rendering algorithms and sensor response models. |
| `datasets` | Dataset generation, parameter sampling and orchestration of particle generation, imaging and dataset assembly. |
| `io` | Reading and writing supported file formats including Zarr, STL, OBJ and configuration files. |
| `viewer` | Interactive inspection and quality assurance of generated geometries and datasets. |

---

# Core Domain Model

HydrometeorSynth separates **geometry** from **physical state**.

A `Geometry` defines only the canonical shape of a particle.

A `Particle` combines a `Geometry` with physical properties including:

- maximum dimension (`Dmax`),
- density,
- orientation,
- position.

Together these represent a single physical particle.

Higher-level workflows such as imaging and dataset generation operate on `Particle` objects rather than directly on meshes or images.

---

# Geometry Model

Geometry represents a canonical shape independent of physical scale.

Physical size is applied by the owning `Particle`.

Geometry implementations may originate from different sources, including:

- procedurally generated geometries,
- imported mesh geometries (for example STL or OBJ files).

Regardless of implementation, all geometry classes present a common public interface.

---

# Geometry Responsibilities

Geometry owns:

- defining parameters,
- parameter validation,
- mesh generation,
- cache lifecycle,
- canonical volume,
- canonical surface area,
- canonical Dmax.

Geometry does **not** own:

- physical Dmax,
- density,
- orientation,
- position,
- imaging,
- random sampling.

---

# Particle Responsibilities

A `Particle` represents the physical state of a single object.

It owns:

- geometry,
- Dmax,
- density,
- orientation,
- position.

It contains only behaviour directly related to its physical state.

`Particle` does not perform:

- geometry generation,
- rendering,
- imaging,
- random sampling,
- dataset generation.

---

# Imaging Model

The imaging package simulates the observation of particles by virtual imaging systems.

It is composed of three primary concepts:

- `Camera`, which defines the viewing geometry,
- `Renderer`, which projects particles into image space,
- `Image`, which stores the rendered pixel data.

The imaging package is independent of dataset generation and may be used by interactive applications or other workflows.

---

# Imaging Responsibilities

The imaging package owns:

- camera models,
- image buffers,
- rendering algorithms,
- sensor response models.

It does **not** own:

- particle generation,
- dataset generation,
- persistent storage,
- visualisation.

---

# Caching Policy

Geometry caches computationally expensive derived quantities, including:

- mesh,
- canonical volume,
- canonical surface area.

Cached values are invalidated automatically when defining parameters change and are recomputed lazily.

`Particle` performs no caching because its derived properties require only inexpensive arithmetic.

---

# Architectural Principles

## Store facts; derive everything else.

Store only fundamental state and derive all secondary properties.

## Separate canonical geometry from physical state.

Shape and physical properties are modelled independently.

## Cache only expensive computations.

Caching is applied only where it provides meaningful computational benefit.

## Prefer composition over inheritance.

Objects collaborate through composition wherever practical.

## Prefer explicit construction over unnecessary abstraction.

Simple, explicit object creation is preferred over introducing abstractions without clear benefit.

## Keep common scientific workflows simple.

The common workflow should remain intuitive while still supporting advanced scientific use cases.

## Layered architecture

Higher-level components coordinate lower-level components without duplicating their responsibilities. Domain objects remain independent of imaging, while imaging remains independent of dataset generation and persistence.

## Streaming processing

Dataset generation follows a streaming model.

Particles are generated, processed, imaged, written to disk and discarded without retaining large collections in memory.

## Parallel execution

The architecture supports parallel generation of independent particles.

Components should avoid unnecessary shared mutable state to enable efficient execution across multiple processes.

## Separation of responsibilities

Geometry, particle modelling, imaging, dataset generation, file I/O and visualisation remain independent components with clearly defined responsibilities.

---

# Package Relationships

The primary dependency relationships are:

```text
datasets
    │
    ├── particle
    ├── imaging
    └── io

imaging
    │
    └── particle

particle
    │
    └── geometry

viewer
    ├── imaging
    └── particle
```

The `datasets` package acts as the primary orchestration layer for synthetic dataset generation, coordinating particle creation, image generation and dataset assembly while delegating specialist tasks to the appropriate packages.

---

# Canonical Geometry Conventions

- All geometries are centred on the origin.
- Each geometry defines a fixed local coordinate system.
- Local axes are chosen for convenience and consistency.
- `Particle.orientation` transforms the canonical geometry into world coordinates.
- Individual geometry classes document their own local axis conventions.

---

# Future Evolution

The architecture is intended to support future extension while maintaining a stable public API.

Expected future developments include:

- additional hydrometeor geometries,
- engineering reference particles,
- additional camera models,
- improved rendering algorithms,
- improved sensor response models,
- expanded physical property calculations,
- additional dataset formats,
- enhanced visualisation capabilities.

New functionality should extend the existing architecture wherever practical rather than introducing unnecessary top-level components.