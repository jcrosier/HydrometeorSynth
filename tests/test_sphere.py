from math import pi
from scipy.spatial.distance import pdist
from trimesh import Trimesh
import pytest
from hydrometeorsynth.geometry.sphere import Sphere


def test_sphere_dmax():
    sphere = Sphere()
    assert sphere.dmax == 2.0


def test_sphere_volume():
    sphere = Sphere()
    assert abs(sphere.volume - (4.0 * pi / 3.0))  < 0.15


def test_sphere_surface_area():
    sphere = Sphere()
    assert abs(sphere.surface_area - (4.0 * pi))  < 0.25


def test_sphere_mesh():
    sphere = Sphere()
    assert isinstance(sphere.mesh, Trimesh)


def test_sphere_analytical_dmax():
    sphere = Sphere()
    hull = sphere.mesh.convex_hull
    mesh_dmax = pdist(hull.vertices).max()
    assert mesh_dmax == pytest.approx(sphere.dmax, rel=1e-3)