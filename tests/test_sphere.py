from math import pi
from scipy.spatial.distance import pdist
from trimesh import Trimesh
import pytest
from hydrometeorsynth.geometry.sphere import Sphere

CANONICAL_RADIUS = 1.0
CANONICAL_DIAMETER = 2.0 * CANONICAL_RADIUS
CANONICAL_VOLUME = 4.0 * pi * CANONICAL_RADIUS**3 / 3.0
CANONICAL_SURFACE_AREA = 4.0 * pi * CANONICAL_RADIUS**2


def test_sphere_dmax():
    sphere = Sphere()
    assert sphere.dmax == CANONICAL_DIAMETER


def test_sphere_volume():
    sphere = Sphere()
    assert sphere.volume == pytest.approx(CANONICAL_VOLUME, abs=0.15)


def test_sphere_surface_area():
    sphere = Sphere()
    assert sphere.surface_area == pytest.approx(CANONICAL_SURFACE_AREA, abs=0.25)


def test_sphere_mesh_type():
    sphere = Sphere()
    assert isinstance(sphere.mesh, Trimesh)


def test_sphere_analytical_vs_mesh_dmax():
    sphere = Sphere()
    hull = sphere.mesh.convex_hull
    mesh_dmax = pdist(hull.vertices).max()
    assert mesh_dmax == pytest.approx(sphere.dmax, rel=1e-3)