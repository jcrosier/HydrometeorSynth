# Architecture

**Project:** HydrometeorSynth

**Version:** Draft 0.1

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
| `imaging` | Camera models, projection algorithms and sensor response models. |
| `datasets` | Dataset generation, parameter sampling, metadata assembly and orchestration of image generation. |
| `io` | Reading and writing supported file formats including Zarr, STL, OBJ and configuration files. |
| `viewer` | Interactive inspection and quality assurance of generated geometries and datasets. |

---

# Core Domain Model

HydrometeorSynth separates **geometry** from **physical state**.

A `Geometry` defines only the shape of a particle.

A `Particle` combines a `Geometry` with physical properties including:

- maximum dimension (`Dmax`),
- density,
- orientation.

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
- canonical surface area.
- canonical Dmax.

Geometry does **not** own:

- physical Dmax,
- density,
- orientation,
- imaging,
- random sampling.

---

# Particle Responsibilities

A `Particle` represents the physical state of a single object.

It owns:

- geometry,
- Dmax,
- density,
- orientation.

It derives physical properties from these values and intentionally contains minimal behaviour.

`Particle` does not perform:

- geometry generation,
- rendering,
- imaging,
- random sampling,
- dataset generation.

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

particle
    │
    └── geometry

viewer
    ├── particle
    └── geometry
```

The `datasets` package acts as the primary orchestration layer for synthetic dataset generation, coordinating particle creation, image generation and dataset assembly while delegating specialist tasks to the appropriate packages.

---

# Future Evolution

The architecture is intended to support future extension while maintaining a stable public API.

Expected future developments include:

- additional hydrometeor geometries,
- engineering reference particles,
- improved camera and sensor response models,
- expanded physical property calculations,
- additional dataset formats,
- enhanced visualisation capabilities.

New functionality should extend the existing architecture wherever practical rather than introducing unnecessary top-level components.