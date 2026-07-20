from math import sqrt
from trimesh.creation import box
from hydrometeorsynth.geometry.base import Geometry

class Cube(Geometry):
    """Canonical cube with unit side length."""

    @property
    def dmax(self) -> float:
        """Canonical dmax for unit cube"""
        return sqrt(3.0)
    
    def _build_mesh(self):
        """Canonical mesh for unit cube"""
        return box(extents=(1.0, 1.0, 1.0))