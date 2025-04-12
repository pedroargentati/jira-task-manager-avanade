from abc import ABC, abstractmethod

class DatabasePort(ABC):
    @abstractmethod
    def buscar_tasks(self, tp_comp: str):
        """Retorna as tasks filtradas por tipo de aplicação"""
        pass
