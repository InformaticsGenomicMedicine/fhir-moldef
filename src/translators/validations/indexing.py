from exceptions.utils import (
    InvalidCoordinateSystemError,
)


def apply_indexing(coord_system, start):
    """Adjust the indexing based on the coordinate system.

    Args:
        CoordSystem (str): The coordinate system, which can be one of the following:
                            '0-based interval counting', '0-based character counting', '1-based character counting'.
        start (int): The start position to be adjusted.

    Raises:
        ValueError: If an invalid coordinate system is specified.

    Returns:
        int: The adjusted start position.

    """
    adjustments = {
        "0-based interval counting": 0,
        "0-based character counting": 1,
        "1-based character counting": -1,
    }

    if coord_system not in adjustments:
        raise InvalidCoordinateSystemError(
            "Invalid coordinate system specified. Valid options are: '0-based interval counting', '0-based character counting', '1-based character counting'."
        )

    return start + adjustments[coord_system]
