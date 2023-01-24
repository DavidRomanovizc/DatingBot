import pathlib
from typing import NoReturn, Union

from loader import detector, classifier


async def classification_image(image_path: Union[str, pathlib.Path]) -> classifier:
    return classifier.classify(image_path)


async def generate_censored_image(image_path: Union[str, pathlib.Path], out_path: Union[str, pathlib.Path]) -> NoReturn:
    detector.censor(
        img_path=image_path,
        out_path=out_path,
        visualize=False
    )
