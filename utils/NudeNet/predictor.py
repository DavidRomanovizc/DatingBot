import pathlib
from typing import (
    Union,
)

from loader import (
    detector,
)


async def classification_image(image_path: Union[str, pathlib.Path]) -> list[dict]:
    return detector.detect(image_path)


async def generate_censored_image(
        image_path: Union[str, pathlib.Path], out_path: Union[str, pathlib.Path]
) -> None:
    detector.censor(
        image_path=image_path,
        output_path=out_path,
    )
