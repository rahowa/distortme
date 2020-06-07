import os
from typing import Iterator, Sequence, Tuple, Optional


def images(folder: str, formats: Optional[Sequence[str]] = None) -> Tuple[str, ...]:
    if not formats:
        formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return tuple(filter(lambda x: x.endswith(formats), os.listdir(folder)))


def directories(folder: str) -> Tuple[str, ...]:
    return tuple(filter(lambda x: os.path.isdir(os.path.join(folder, x)),
                        os.listdir(folder)))


def current_dir() -> str:
    return os.getcwd()


def full_path(names: Sequence[str], imgdir: str) -> Iterator[str]:
    return (os.path.join(imgdir, name) for name in names)


def create_folders(names: Sequence[str]) -> None:
    missed_folders = filter(lambda x: not os.path.exists(x), names)
    for folder in missed_folders:
        os.mkdir(folder)
