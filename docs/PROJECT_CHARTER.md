# Project Charter

**Project:** HydrometeorSynth

**Version:** Draft 0.1

**Status:** In Development

## Vision

HydrometeorSynth is an open-source Python framework for generating synthetic multi-view images of hydrometeors and other three-dimensional particles for machine learning, computer vision, and atmospheric science.

The project aims to provide physically plausible particle geometries, configurable imaging systems, and reproducible datasets suitable for algorithm development, validation, and scientific research.

## Goals

HydrometeorSynth aims to:

- Generate physically plausible three-dimensional particle geometries, with a focus on atmospheric hydrometeors.
- Support liquid, ice, snow, and mixed-phase hydrometeors.
- Generate configurable orthographic multi-view images.
- Produce reproducible machine-learning datasets using modern, structured data formats (initially Zarr) suitable for local and cloud-based workflows.
- Support imported engineering objects for validation and benchmarking.
- Provide scientifically meaningful metadata describing particle geometry and physical properties.
- Be an open-source, community-driven scientific software project.

## Scope

HydrometeorSynth is intended to support research, development and education in atmospheric particle imaging and machine learning.

The project focuses on generating synthetic datasets from physically plausible particle geometries and configurable imaging systems. Atmospheric hydrometeors are the primary application domain, while imported engineering objects are supported for validation, benchmarking and camera characterisation.

HydrometeorSynth is not intended to model cloud microphysical processes, particle growth, radiative transfer or light scattering, although future extensions may interface with external models.

## Guiding Principles

HydrometeorSynth is developed according to the following principles:

1. **Scientific credibility** — Models should be physically plausible and scientifically defensible.

2. **Reproducibility** — All datasets should be reproducible from recorded configuration, parameters and random seeds.

3. **Modularity** — Geometry, physics, orientation, imaging and dataset generation should remain independent components wherever practical.

4. **Extensibility** — New particle types, imaging systems and physics models should be straightforward to add without modifying the core framework.

5. **Validation** — New functionality should be accompanied by appropriate validation against analytical solutions, engineering reference objects or published scientific observations.

6. **Open science** — The project will be developed openly with comprehensive documentation, testing and version control.

7. **Performance** — Optimise where it provides meaningful benefit, while maintaining code readability, maintainability and scientific correctness.

## Governance

HydrometeorSynth is developed as an open-source scientific software project.

Development is guided by the principles described in this charter, with an emphasis on scientific credibility, reproducibility, transparency and community contribution.

Major architectural decisions should be documented using Architecture Decision Records (ADRs). New features should include appropriate documentation, testing and validation before being incorporated into the main development branch.

## Long-term Vision

HydrometeorSynth aims to become a community-developed platform for the generation of synthetic hydrometeor datasets for atmospheric science and machine learning.

Future development is expected to include:

- Additional hydrometeor particle types and parameterisations.
- More sophisticated imaging and camera response models.
- Expanded physical property calculations.
- Validation against laboratory and field observations.
- Tools for dataset inspection, visualisation and quality assurance.
- Interfaces for machine-learning workflows and scientific analysis.

The project will evolve through open development, community feedback and scientific validation while maintaining backwards compatibility wherever practical.