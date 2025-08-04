"""
Objeto de valor TranscriptionPlan.
Define a estratégia de IA e fallback para transcrição.
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class TranscriptionPlan:
    """
    Objeto de valor que define um plano de transcrição.
    
    Attributes:
        transcriber_names: Lista ordenada de nomes de transcribers para tentar
        max_retries: Número máximo de tentativas por transcriber
        timeout_seconds: Timeout em segundos para cada tentativa
        options: Opções específicas para configurar os transcribers
    """
    transcriber_names: List[str]
    max_retries: int = 1
    timeout_seconds: int = 300  # 5 minutos
    options: Dict[str, Any] = None
    
    def __post_init__(self):
        """Valida os parâmetros do plano."""
        if not self.transcriber_names:
            raise ValueError("Pelo menos um transcriber deve ser especificado")
        
        if self.max_retries < 1:
            raise ValueError("Número de tentativas deve ser pelo menos 1")
        
        if self.timeout_seconds <= 0:
            raise ValueError("Timeout deve ser positivo")
        
        if self.options is None:
            object.__setattr__(self, 'options', {})
    
    @property
    def primary_transcriber(self) -> str:
        """Retorna o transcriber primário (primeiro da lista)."""
        return self.transcriber_names[0]
    
    @property
    def has_fallback(self) -> bool:
        """Verifica se há transcribers de fallback."""
        return len(self.transcriber_names) > 1
    
    @property
    def fallback_transcribers(self) -> List[str]:
        """Retorna a lista de transcribers de fallback."""
        return self.transcriber_names[1:] if self.has_fallback else []
    
    def get_transcriber_options(self, transcriber_name: str) -> Dict[str, Any]:
        """
        Retorna as opções específicas para um transcriber.
        
        Args:
            transcriber_name: Nome do transcriber
            
        Returns:
            Dicionário com as opções do transcriber
        """
        return self.options.get(transcriber_name, {})
    
    @classmethod
    def create_simple(cls, primary_transcriber: str, fallback_transcriber: str = None) -> 'TranscriptionPlan':
        """
        Factory method para criar um plano simples.
        
        Args:
            primary_transcriber: Transcriber primário
            fallback_transcriber: Transcriber de fallback (opcional)
            
        Returns:
            Novo TranscriptionPlan
        """
        transcribers = [primary_transcriber]
        if fallback_transcriber:
            transcribers.append(fallback_transcriber)
        
        return cls(transcriber_names=transcribers)
    
    @classmethod
    def create_with_multiple_fallbacks(cls, transcribers: List[str], **kwargs) -> 'TranscriptionPlan':
        """
        Factory method para criar um plano com múltiplos fallbacks.
        
        Args:
            transcribers: Lista de transcribers em ordem de prioridade
            **kwargs: Outros parâmetros do plano
            
        Returns:
            Novo TranscriptionPlan
        """
        return cls(transcriber_names=transcribers, **kwargs)
