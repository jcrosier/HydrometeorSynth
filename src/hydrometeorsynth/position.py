from math import isfinite


class Position:
    """Represents the position of a particle in three-dimensional space."""
    def __init__(self, *, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return (
            f"Position("
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z})"
        )

    def _validate_position(self, name: str, value: float | int) -> float:
        if isinstance(value, bool)  or not isinstance(value, (float, int)):
            raise TypeError(f"{name} must be an int or float")
        if not isfinite(value):
            raise ValueError(f"{name} must be a real number")
        return float(value)
    
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float | int):
        self._x = self._validate_input("x", value)

    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value: float | int):
        self._y = self._validate_input("y", value)

    @property
    def z(self) -> float:
        return self._z
    
    @z.setter
    def z(self, value: float | int):
        self._z = self._validate_input("z", value)