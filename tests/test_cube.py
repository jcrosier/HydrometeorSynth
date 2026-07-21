from math import sqrt

import pytest
from scipy.spatial.distance import pdist
from trimesh import Trimesh

from hydrometeorsynth.geometry.cube import Cube

CANONICAL_LENGTH = 1.0
CANONICAL_VOLUME = CANONICAL_LENGTH**3
CANONICAL_SURFACE_AREA = 6.0 * CANONICAL_LENGTH**2


def test_cube_dmax():
    unit_cube = Cube()
    assert unit_cube.dmax == CANONICAL_LENGTH * sqrt(3.0)


def test_cube_volume():
    unit_cube = Cube()
    assert unit_cube.volume == pytest.approx(CANONICAL_VOLUME)


def test_cube_surface_area():
    unit_cube = Cube()
    assert unit_cube.surface_area == pytest.approx(CANONICAL_SURFACE_AREA)


def test_cube_mesh_type():
    cube = Cube()
    assert isinstance(cube.mesh, Trimesh)


def test_cube_analytical_dmax():
    cube = Cube()
    hull = cube.mesh.convex_hull
    mesh_dmax = pdist(hull.vertices).max()
    assert mesh_dmax == pytest.approx(cube.dmax, rel=1e-3)
