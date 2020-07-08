import numpy as np


ImageType = np.ndarray  # Data type for exmaple


def map_fn(entity: ImageType) -> ImageType:
    """
    Example of custom map function
    [ATTENTION]
        *  ImageType should be np.ndarray or anything that OpenCV can handle
        *  Name of your functon should be exactly 'map_fn'
        *  Function should return element the same type that accept
    Parameters
    ----------
        entity: DataSample
            One sample from dataset which will be modified

    Return
    ------
        resutl: ImageType
            Modified image
    """

    result = entity.copy()
    return result


