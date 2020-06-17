import json
from typing import Sequence

from distortme.base_types import BaseResult


def save_results(result_file: str, files: Sequence[str], results: Sequence[BaseResult]) -> None:
    result_dict = {file: res.to_dict(file) for file, res in zip(files, results)}
    with open(result_file, 'w') as res_json: 
        json.dump(result_dict, res_json)
