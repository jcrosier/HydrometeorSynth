from math import sqrt

from trimesh.creation import box

from hydrometeorsynth.geometry.base import Geometry

CANONICAL_LENGTH = 1.0


class Cube(Geometry):
    """Canonical cube centred at the origin with unit side length."""

    @property
    def dmax(self) -> float:
        """Canonical dmax for unit cube."""
        return CANONICAL_LENGTH * sqrt(3.0)

    def _build_mesh(self):
        """Build and return the mesh for the canonical cube."""
        return box(extents=(CANONICAL_LENGTH, CANONICAL_LENGTH, CANONICAL_LENGTH))
