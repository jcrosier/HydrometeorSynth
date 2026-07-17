from hydrometeorsynth.geometry.base import Geometry
from trimesh.creation import box


class DummyGeometry(Geometry):
    """Minimal concrete Geometry used for testing the Geometry base class."""

    def __init__(self):
        super().__init__()
        self.build_count = 0

    def _build_mesh(self):
        self.build_count += 1
        return box(extents=(1.0, 1.0, 1.0))
        
def test_mesh_is_built_only_once():
    geometry = DummyGeometry()
    assert geometry.build_count == 0
    _ = geometry.mesh
    assert geometry.build_count == 1
    _ = geometry.mesh
    assert geometry.build_count == 1

def test_volume_uses_cached_mesh():
    geometry = DummyGeometry()
    assert geometry.build_count == 0
    _ = geometry.volume
    assert geometry.build_count == 1
    _ = geometry.volume
    assert geometry.build_count == 1

def test_surface_area_uses_cached_mesh():
    geometry = DummyGeometry()
    assert geometry.build_count == 0
    _ = geometry.surface_area
    assert geometry.build_count == 1
    _ = geometry.surface_area
    assert geometry.build_count == 1

def test_mesh_cache_invalidation():
    geometry = DummyGeometry()
    _ = geometry.mesh
    assert geometry.build_count == 1
    geometry._geometry_changed()
    _ = geometry.mesh
    assert geometry.build_count == 2

def test_volume_cache_invalidation():
    geometry = DummyGeometry()
    _ = geometry.volume
    assert geometry.build_count == 1
    geometry._geometry_changed()
    _ = geometry.volume
    assert geometry.build_count == 2

def test_surface_area_cache_invalidation():
    geometry = DummyGeometry()
    _ = geometry.surface_area
    assert geometry.build_count == 1
    geometry._geometry_changed()
    _ = geometry.surface_area
    assert geometry.build_count == 2