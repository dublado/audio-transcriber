"""
Registry de Transcribers.
Implementa padrão Service Locator para gerenciar instâncias de transcribers.
"""
from typing import Dict, Optional, List

from ...domain.interfaces.transcriber import Transcriber


class TranscriberRegistry:
    """
    Registry responsável por gerenciar instâncias de transcribers.
    
    Implementa o padrão Service Locator, fornecendo um ponto central
    para obter instâncias de transcribers em tempo de execução.
    """
    
    def __init__(self):
        """Inicializa o registry vazio."""
        self._transcribers: Dict[str, Transcriber] = {}
    
    def register(self, transcriber: Transcriber) -> None:
        """
        Registra um transcriber no registry.
        
        Args:
            transcriber: Instância do transcriber a ser registrado
            
        Raises:
            ValueError: Se já existe um transcriber com o mesmo nome
        """
        name = transcriber.get_name()
        
        if name in self._transcribers:
            raise ValueError(f"Transcriber '{name}' já está registrado")
        
        self._transcribers[name] = transcriber
    
    def unregister(self, name: str) -> bool:
        """
        Remove um transcriber do registry.
        
        Args:
            name: Nome do transcriber a ser removido
            
        Returns:
            True se removido, False se não existia
        """
        if name in self._transcribers:
            del self._transcribers[name]
            return True
        return False
    
    def get_transcriber(self, name: str) -> Optional[Transcriber]:
        """
        Obtém uma instância de transcriber pelo nome.
        
        Args:
            name: Nome do transcriber desejado
            
        Returns:
            Instância do transcriber ou None se não encontrado
        """
        return self._transcribers.get(name)
    
    def list_names(self) -> List[str]:
        """
        Lista todos os nomes de transcribers registrados.
        
        Returns:
            Lista com os nomes dos transcribers
        """
        return list(self._transcribers.keys())
    
    def list_available(self) -> List[str]:
        """
        Lista nomes dos transcribers que estão disponíveis.
        
        Returns:
            Lista com nomes dos transcribers disponíveis
        """
        available = []
        for name, transcriber in self._transcribers.items():
            if transcriber.is_available():
                available.append(name)
        return available
    
    def has_transcriber(self, name: str) -> bool:
        """
        Verifica se um transcriber está registrado.
        
        Args:
            name: Nome do transcriber
            
        Returns:
            True se registrado, False caso contrário
        """
        return name in self._transcribers
    
    def clear(self) -> None:
        """Remove todos os transcribers do registry."""
        self._transcribers.clear()
    
    def count(self) -> int:
        """
        Retorna o número de transcribers registrados.
        
        Returns:
            Quantidade de transcribers
        """
        return len(self._transcribers)
    
    def get_transcribers_for_format(self, audio_format: str) -> List[Transcriber]:
        """
        Obtém todos os transcribers que suportam um formato específico.
        
        Args:
            audio_format: Formato de áudio (mp3, wav, etc.)
            
        Returns:
            Lista de transcribers que suportam o formato
        """
        compatible = []
        for transcriber in self._transcribers.values():
            if transcriber.supports_format(audio_format):
                compatible.append(transcriber)
        return compatible
