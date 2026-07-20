from math import pi
from trimesh import Trimesh
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