from math import isfinite

from hydrometeorsynth.geometry.base import Geometry
from hydrometeorsynth.orientation import Orientation

# todo: import Orientation and integrate Orientation type
MIN_DMAX = 0.01
MAX_DMAX = 100.0

MIN_DENSITY = 100.0
MAX_DENSITY = 1500.0


class Particle:
    """Represents a physical hydrometeor with a canonical geometry,
    physical size, density and orientation..
    Particles must specify Geometry from /geometry.
    Particles must specify dmax: units are mm (millimeters).
        valid range: 0.01 and 100.0 (mm)
    Particles must specify density: units are kg/m-3.
        valid range: 100 to 1500 (kg/m-3)
    Particles have orientation:
        None: default orientation
        Orientation: object specifying Euler angles (phi, theta, psi) in degrees
    Particles reference an underlying Geometry object.
    Geometry is responsible for mesh generation and caching.
    Particle does not cache derived properties.
    """

    def __init__(
        self,
        geometry: Geometry,
        dmax: float,
        density: float,
        orientation: Orientation | None = None,
    ):
        self.geometry = geometry
        self.dmax = dmax
        self.density = density
        self.orientation = orientation

    @property
    def geometry(self) -> Geometry:
        return self._geometry

    @geometry.setter
    def geometry(self, value: Geometry) -> None:
        if not isinstance(value, Geometry):
            raise TypeError("geometry must be of Geometry type")
        self._geometry = value

    @property
    def dmax(self) -> float:
        return self._dmax

    @dmax.setter
    def dmax(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("dmax needs to type int or float")
        if not isfinite(value):
            raise ValueError("dmax must be a real number")
        if not MIN_DMAX <= value <= MAX_DMAX:
            raise ValueError(f"dmax must be between {MIN_DMAX} and {MAX_DMAX} (mm)")
        self._dmax = float(value)

    @property
    def density(self) -> float:
        return self._density

    @density.setter
    def density(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("density needs to type int or float")
        if not isfinite(value):
            raise ValueError("density must be a real number")
        if not MIN_DENSITY <= value <= MAX_DENSITY:
            raise ValueError(
                f"density must be between {MIN_DENSITY} \
                             and {MAX_DENSITY} (kg/m-3)"
            )
        self._density = float(value)

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @orientation.setter
    def orientation(self, value: Orientation | None) -> None:
        if value is None:
            self._orientation = Orientation()
        elif isinstance(value, Orientation):
            self._orientation = value
        else:
            raise TypeError("orientation must be of Orientation type")

    @property
    def scale(self) -> float:
        return self.dmax / self.geometry.dmax

    @property
    def surface_area(self) -> float:
        return self.geometry.surface_area * (self.scale**2)

    @property
    def volume(self) -> float:
        return self.geometry.volume * (self.scale**3)

    @property
    def mass(self) -> float:
        return self.volume * self.density
