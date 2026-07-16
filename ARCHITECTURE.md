# Architecture

**Project:** HydrometeorSynth

**Version:** Draft 0.1

---

# Purpose

This document describes the high-level software architecture of HydrometeorSynth.

It defines the major software components, their responsibilities and interactions. It does not describe implementation details, algorithms or individual class designs, which will be documented separately as the project evolves.

This document describes the current architecture of HydrometeorSynth.

The rationale for significant architectural decisions is documented separately using Architecture Decision Records (ADRs).

---

# High-Level Architecture

HydrometeorSynth is organised into a small number of high-level components, each with a clearly defined responsibility.

| Component | Responsibility |
|-----------|----------------|
| `geometry` | Geometric representations, mesh generation, transformations and geometric calculations. |
| `particles` | Particle definitions including atmospheric hydrometeors and engineering reference particles. |
| `imaging` | Camera models, projection algorithms and sensor response models. |
| `datasets` | Dataset generation, sampling strategies, metadata assembly and orchestration of multi-view image generation. |
| `io` | Reading and writing supported file formats including Zarr, STL, OBJ and configuration files. |
| `viewer` | Interactive inspection and quality assurance of generated datasets. |

---

# Central Domain Object

The central domain object within HydrometeorSynth is the **Particle**.

Particles are the fundamental entities manipulated throughout the framework. Geometry generation, imaging, dataset generation and metadata all operate on particles rather than directly on meshes or images.

The software architecture therefore follows a particle-centric design.

---

# Particle Model

A particle is defined by two fundamental characteristics:

- **Geometry** — the particle shape.
- **Material** — the physical substance from which the particle is composed.

Additional information such as orientation, metadata and derived physical properties are associated with the particle but do not define its identity.

The geometry associated with a particle may originate from different sources, including:

- Procedurally generated geometries.
- Imported mesh geometries (e.g. STL or OBJ).

These different geometry implementations should present a common interface to the remainder of the framework.

---

# Architectural Principles

HydrometeorSynth is designed according to the following architectural principles.

## Particle-centric

The `Particle` is the central domain object. All generation, imaging and dataset creation workflows operate on particles.

## Immutable particles

Particles are immutable after creation.

Parameter sweeps and stochastic generation create new particle instances rather than modifying existing particles.

## Streaming processing

The primary processing model is streaming.

Particles are generated, processed, imaged, written to disk and discarded without requiring large numbers of meshes to remain simultaneously in memory.

## Parallel execution

The architecture shall support parallel generation of independent particles.

Components should avoid shared mutable state, allowing efficient execution across multiple CPU processes.

The architecture describes the capability for parallel execution rather than a specific implementation technology.

## Separation of responsibilities

Geometry, particle definitions, imaging, dataset generation, file I/O and visualisation remain independent components with clearly defined responsibilities.

## User-oriented design

Packages are organised around user-facing responsibilities rather than purely internal implementation details.

---

# Package Relationships

The major package interactions are illustrated below.

FILL THIS IN

The `datasets` package acts as the primary orchestration layer for synthetic dataset generation, coordinating particle creation, image generation and dataset assembly while delegating specialist tasks to the appropriate packages.

---

# Future Evolution

The architecture is intended to support future extension while maintaining a stable public API.

Expected future developments include:

- Additional hydrometeor particle models.
- Additional engineering reference particles.
- Improved camera and sensor response models.
- Expanded physical property calculations.
- Additional dataset formats.
- Additional visualisation capabilities.

New functionality should extend the existing architecture wherever practical rather than introducing unnecessary top-level components.
