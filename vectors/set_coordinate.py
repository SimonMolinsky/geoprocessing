def set_coordinate(point_geometry, coordinate: str):
    """
    Function returns coordinate x or y from multipoint geometry in geodataframe.
    :param point_geometry: MultiPoint or Point geometry,
    :param coordinate: x (longitude) or y (latitude).
    """
     
    if coordinate == 'x':
        try:
            x_coo = point_geometry.x
            return x_coo
        except AttributeError:
            x_coo = point_geometry[0].x
            return x_coo
    elif coordinate == 'y':
        try:
            y_coo = point_geometry.y
            return y_coo
        except AttributeError:
            y_coo = point_geometry[0].y
            return y_coo
    else:
        raise KeyError('Available coordinates: "x" for longitude or "y" for latitude')
