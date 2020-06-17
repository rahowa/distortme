import os
from tqdm import tqdm
from frozendict import frozendict
from typing import Callable, Sequence

from src.main_utils import print_delimiter


def unpack_command(command: str) -> Callable[[str], None]:
    def unpack_file(filename: str) -> None:
        os.system(f"{command} {filename}")
    return unpack_file


EXTENSION_TO_COMMAND = frozendict({
            ".tar.bz2": unpack_command("tar xvjf"),
            ".tar.gz": unpack_command("tar xvzf"),
            ".bz2": unpack_command("bunzip2"),
            ".rar": unpack_command("unrar x"),
            ".gz": unpack_command("gunzip"),
            ".tar": unpack_command("tar xvf"),
            ".tbz2": unpack_command("tar xvjf"),
            ".tgz": unpack_command("tar xvzf"),
            ".zip": unpack_command("unzip"),
            ".Z)": unpack_command("uncompress"),
            ".7z": unpack_command("7z x")
})


@print_delimiter("Unpack archives")
def main_unpack(files: Sequence[str]) -> None:
    pbar = tqdm(files, ncols=80)
    for path_to_file in pbar:
        filename, file_extension = os.path.splitext(path_to_file)
        EXTENSION_TO_COMMAND[file_extension](path_to_file)
        pbar.set_description(f"Unpack file: [{os.path.basename(filename)}]")
