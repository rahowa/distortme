import os
import aiohttp
import asyncio
from tqdm import tqdm
from typing import Sequence, Dict
from distortme.datasets import Datasets, DATASET_DOWNLOAD_LINKS
from distortme.files_utils import create_folders
from distortme.main_utils import print_delimiter_async


class Downloader:
    def __init__(self, urls: Dict[str, str], path: str, tag: str = "Dataset"):
        self.urls = urls
        self.tag = tag
        self.path = path

    async def _download_dataset(self, session: aiohttp.ClientSession, url: str, path: str, tag: str) -> None:
        chunk_size = 1024
        filename = url.split('/')[-1]
        path_to_save = os.path.join(path, filename)
        async with session.get(url) as resp:
            total_chunks = resp.headers['CONTENT-LENGTH']
            with open(path_to_save, 'wb') as file:
                pbar = tqdm(total=int(total_chunks), desc=tag, ncols=80)
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    pbar.update(chunk_size)
                pbar.close()

    async def download(self, session: aiohttp.ClientSession, key: str, tag: str):
        await self._download_dataset(session, self.urls[key], self.path, tag)

    def future(self, sess: aiohttp.ClientSession) -> asyncio.Future:
        tasks = (self.download(sess, key, self.tag + f" [{key}]") for key in self.urls.keys())
        return asyncio.gather(*tasks)


@print_delimiter_async("Download provided datasets...")
async def main_download(datasets: Sequence[Datasets], folder: str):
    save_folder = "Dataset_" + "_".join((dataset.value for dataset in datasets))
    save_folder = os.path.join(folder, save_folder)
    paths = tuple(os.path.join(save_folder, dataset.value) for dataset in datasets)
    create_folders((save_folder, ))
    create_folders(paths)
    async with aiohttp.ClientSession() as session:
        tasks = (Downloader(DATASET_DOWNLOAD_LINKS[ds.value], paths[idx], ds.value).future(session)
                 for idx, ds in enumerate(datasets))
        await asyncio.gather(*tasks)
