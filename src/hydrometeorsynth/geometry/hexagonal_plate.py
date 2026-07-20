from math import sqrt, isfinite
from shapely.geometry import Polygon
from trimesh.creation import extrude_polygon
import numpy as np
from hydrometeorsynth.geometry.base import Geometry

class HexagonalPlate(Geometry):
    """Canonical hexagonal plate with vertices at unit circumradius.

    Centroid at (0, 0, 0).

    Aspect ratio is defined as thickness / diameter.

    Basal face lies in the x-y plane, with the c-axis along +z.

    Thickness extends from -t/2 to +t/2.

    Vertices are numbered counter-clockwise from the +x axis.
    """
    
    def __init__(self, aspect_ratio: float = 0.1):
        super().__init__()
        self.aspect_ratio = aspect_ratio

    @property
    def aspect_ratio(self) -> float:
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Aspect ratio must be a real number.")
        if not (isfinite(value) and value > 0.0):
            raise ValueError("Aspect ratio must be a finite value > 0.")
        current = getattr(self, "_aspect_ratio", None)
        if value != current:
            self._aspect_ratio = float(value)
            self._geometry_changed()

    @property
    def dmax(self) -> float:
        """Canonical dmax for hexagonal plate with circumradius of 1"""
        diameter = 2.0
        thickness: float = self.aspect_ratio * diameter
        return sqrt(diameter**2 + thickness**2)
    
    def _build_mesh(self):
        """Canonical mesh for hexagonal plate"""
        diameter = 2.0
        thickness = self.aspect_ratio * diameter
        angle = np.linspace(0, 2 * np.pi, 7)[:-1]
        hexagon_vertices = np.column_stack((np.cos(angle), np.sin(angle)))
        poly = Polygon(hexagon_vertices)
        return extrude_polygon(poly, height=thickness).apply_translation([0, 0, -0.5*thickness])