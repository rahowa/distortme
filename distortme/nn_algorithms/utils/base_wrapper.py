from abc import ABC, abstractmethod
from typing import List

from distortme.base_types import BaseResult


class BaseWrapper(ABC):
    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def load(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def preprocess(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def predict(self, *args, **kwargs) -> List[BaseResult]:
        raise NotImplementedError

