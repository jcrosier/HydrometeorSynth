from math import sqrt
from scipy.spatial.distance import pdist
import pytest
from hydrometeorsynth.geometry.cube import Cube


def test_cube_dmax():
    unit_cube = Cube()
    assert unit_cube.dmax == sqrt(3.0)


def test_cube_volume():
    unit_cube = Cube()
    assert unit_cube.volume == 1.0


def test_cube_surface_area():
    unit_cube = Cube()
    assert unit_cube.surface_area == 6.0


def test_cube_analytical_dmax():
    cube = Cube()
    hull = cube.mesh.convex_hull
    mesh_dmax = pdist(hull.vertices).max()
    assert mesh_dmax == pytest.approx(cube.dmax, rel=1e-3)