from abc import ABC, abstractmethod

class JiraPort(ABC):

    @abstractmethod
    def story_exists(self, token: str, story_key: str) -> bool:
        pass