"""
Política de fallback para seleção de transcribers.
Implementa o padrão Strategy para determinar como escolher transcribers.
"""
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ...domain.interfaces.transcriber import Transcriber
    from ...infrastructure.transcribers.registry import TranscriberRegistry


class FallbackPolicy(ABC):
    """
    Interface para políticas de fallback.
    
    Define como resolver a lista de transcribers a serem utilizados
    com base na estratégia implementada.
    """
    
    @abstractmethod
    def resolve(self, transcriber_names: List[str], registry: 'TranscriberRegistry') -> List['Transcriber']:
        """
        Resolve a lista de transcribers disponíveis para uso.
        
        Args:
            transcriber_names: Lista de nomes dos transcribers desejados
            registry: Registry contendo as instâncias dos transcribers
            
        Returns:
            Lista ordenada de transcribers prontos para uso
        """
        pass


class DefaultFallbackPolicy(FallbackPolicy):
    """
    Política de fallback padrão.
    
    Retorna apenas transcribers que estão disponíveis e suportam o formato,
    na ordem especificada.
    """
    
    def resolve(self, transcriber_names: List[str], registry: 'TranscriberRegistry') -> List['Transcriber']:
        """
        Implementação da política padrão.
        
        Filtra apenas transcribers disponíveis e os retorna na ordem original.
        """
        transcribers = []
        
        for name in transcriber_names:
            transcriber = registry.get_transcriber(name)
            if transcriber and transcriber.is_available():
                transcribers.append(transcriber)
        
        return transcribers


class AvailabilityFirstFallbackPolicy(FallbackPolicy):
    """
    Política que prioriza transcribers disponíveis.
    
    Reordena a lista colocando primeiro os transcribers que estão disponíveis,
    independente da ordem original.
    """
    
    def resolve(self, transcriber_names: List[str], registry: 'TranscriberRegistry') -> List['Transcriber']:
        """
        Implementação que prioriza disponibilidade.
        
        Separa transcribers disponíveis e indisponíveis, priorizando os disponíveis.
        """
        available_transcribers = []
        unavailable_transcribers = []
        
        for name in transcriber_names:
            transcriber = registry.get_transcriber(name)
            if transcriber:
                if transcriber.is_available():
                    available_transcribers.append(transcriber)
                else:
                    unavailable_transcribers.append(transcriber)
        
        # Retorna primeiro os disponíveis, depois os indisponíveis
        return available_transcribers + unavailable_transcribers


class FormatAwareFallbackPolicy(FallbackPolicy):
    """
    Política que considera o formato do áudio.
    
    Filtra transcribers que suportam o formato específico do áudio.
    """
    
    def __init__(self, audio_format: str):
        """
        Inicializa a política com o formato de áudio.
        
        Args:
            audio_format: Formato do arquivo de áudio
        """
        self.audio_format = audio_format
    
    def resolve(self, transcriber_names: List[str], registry: 'TranscriberRegistry') -> List['Transcriber']:
        """
        Implementação que considera o formato do áudio.
        
        Filtra apenas transcribers que suportam o formato especificado.
        """
        compatible_transcribers = []
        
        for name in transcriber_names:
            transcriber = registry.get_transcriber(name)
            if (transcriber and 
                transcriber.is_available() and 
                transcriber.supports_format(self.audio_format)):
                compatible_transcribers.append(transcriber)
        
        return compatible_transcribers
