from hydrometeorsynth.geometry.base import Geometry
from trimesh.creation import icosphere

class Sphere(Geometry):
    """Canonical sphere with unit radius."""
    
    @property
    def dmax(self):
        """Return the value of Dmax for the canonical sphere with unit radius."""
        return 2.0

    def _build_mesh(self):
        """Build and return the mesh for a canonical sphere with unit radius."""
        return icosphere(radius=1.0, subdivisions=2)