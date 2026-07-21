from abc import ABC, abstractmethod

from trimesh import Trimesh


class Geometry(ABC):
    """Abstract base class for all particle geometries."""

    def __init__(self):
        self._mesh: Trimesh | None = None
        self._volume: float | None = None
        self._surface_area: float | None = None

    @property
    def mesh(self):
        """Return the canonical mesh."""
        if self._mesh is None:
            self._mesh = self._build_mesh()
        return self._mesh

    @property
    def volume(self) -> float:
        """Return the canonical volume."""
        if self._volume is None:
            self._volume = self.mesh.volume
        return self._volume

    @property
    def surface_area(self) -> float:
        """Return the canonical surface area."""
        if self._surface_area is None:
            self._surface_area = self.mesh.area
        return self._surface_area

    @property
    @abstractmethod
    def dmax(self) -> float:
        """Return the maximum dimension of the canonical geometry."""

    @abstractmethod
    def _build_mesh(self) -> Trimesh:
        """Construct and return the canonical mesh."""
        ...

    def _geometry_changed(self):
        """Invalidate cached properties because the geometry has changed."""
        self._mesh = None
        self._volume = None
        self._surface_area = None
