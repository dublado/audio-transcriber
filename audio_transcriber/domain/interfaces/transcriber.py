"""
Interface Transcriber.
Contrato comum para todos os provedores de transcrição de IA.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from ..models.audio_file import AudioFile


class TranscriberException(Exception):
    """Exceção base para erros de transcrição."""
    pass


class TranscriberTimeoutException(TranscriberException):
    """Exceção para timeout na transcrição."""
    pass


class TranscriberUnavailableException(TranscriberException):
    """Exceção quando o transcriber não está disponível."""
    pass


class Transcriber(ABC):
    """
    Interface abstrata para transcribers de áudio.
    
    Todos os adaptadores de provedores de IA devem implementar esta interface.
    """
    
    @abstractmethod
    def transcribe(self, audio_file: AudioFile, options: Dict[str, Any] = None) -> str:
        """
        Transcreve um arquivo de áudio para texto.
        
        Args:
            audio_file: Arquivo de áudio a ser transcrito
            options: Opções específicas do transcriber
            
        Returns:
            Texto transcrito
            
        Raises:
            TranscriberException: Quando ocorre erro na transcrição
            TranscriberTimeoutException: Quando a operação expira
            TranscriberUnavailableException: Quando o serviço está indisponível
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se o transcriber está disponível para uso.
        
        Returns:
            True se disponível, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Retorna o nome identificador do transcriber.
        
        Returns:
            Nome único do transcriber
        """
        pass
    
    @abstractmethod
    def supports_format(self, audio_format: str) -> bool:
        """
        Verifica se o transcriber suporta o formato de áudio.
        
        Args:
            audio_format: Formato do arquivo (mp3, wav, etc.)
            
        Returns:
            True se suportado, False caso contrário
        """
        pass
    
    def validate_audio_file(self, audio_file: AudioFile) -> None:
        """
        Valida se o arquivo de áudio é compatível com o transcriber.
        
        Args:
            audio_file: Arquivo a ser validado
            
        Raises:
            TranscriberException: Se o arquivo não for compatível
        """
        if not self.supports_format(audio_file.format):
            raise TranscriberException(
                f"Formato {audio_file.format} não suportado por {self.get_name()}"
            )
        
        # Validações adicionais podem ser implementadas por subclasses
