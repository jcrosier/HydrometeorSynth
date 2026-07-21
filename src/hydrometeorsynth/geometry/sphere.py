from trimesh.creation import icosphere

from hydrometeorsynth.geometry.base import Geometry

CANONICAL_RADIUS = 1.0
CANONICAL_DIAMETER = 2.0 * CANONICAL_RADIUS


class Sphere(Geometry):
    """Canonical sphere centred at the origin with unit radius."""

    @property
    def dmax(self):
        """Return the value of Dmax for the canonical sphere with unit radius."""
        return CANONICAL_DIAMETER

    def _build_mesh(self):
        """Build and return the mesh for a canonical sphere with unit radius."""
        return icosphere(radius=CANONICAL_RADIUS, subdivisions=2)
