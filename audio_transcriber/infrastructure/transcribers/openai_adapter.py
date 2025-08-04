"""
Adaptador para OpenAI Whisper API.
Implementa a interface Transcriber para o serviço da OpenAI.
"""
import logging
from typing import Dict, Any, List

from ...domain.interfaces.transcriber import (
    Transcriber, 
    TranscriberException, 
    TranscriberTimeoutException,
    TranscriberUnavailableException
)
from ...domain.models.audio_file import AudioFile


logger = logging.getLogger(__name__)


class OpenAIAdapter(Transcriber):
    """
    Adaptador para o serviço de transcrição da OpenAI (Whisper).
    
    Este adaptador simula a integração com a API da OpenAI.
    Em uma implementação real, seria necessário instalar e usar a biblioteca openai.
    """
    
    def __init__(self, api_key: str = None, model: str = "whisper-1"):
        """
        Inicializa o adaptador OpenAI.
        
        Args:
            api_key: Chave da API OpenAI
            model: Modelo a ser usado (whisper-1 é o padrão)
        """
        self.api_key = api_key
        self.model = model
        self._supported_formats = [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"]
    
    def transcribe(self, audio_file: AudioFile, options: Dict[str, Any] = None) -> str:
        """
        Transcreve o arquivo de áudio usando OpenAI Whisper.
        
        Args:
            audio_file: Arquivo de áudio a ser transcrito
            options: Opções específicas (language, temperature, etc.)
            
        Returns:
            Texto transcrito
            
        Raises:
            TranscriberException: Se a transcrição falhar
        """
        if not self.is_available():
            raise TranscriberUnavailableException("OpenAI API não está disponível")
        
        self.validate_audio_file(audio_file)
        
        options = options or {}
        
        try:
            logger.info(f"Transcrevendo {audio_file.filename} com OpenAI Whisper")
            
            # SIMULAÇÃO - Em produção, aqui seria feita a chamada real para a API
            # import openai
            # with open(audio_file.path, "rb") as audio:
            #     response = openai.Audio.transcribe(
            #         model=self.model,
            #         file=audio,
            #         language=options.get("language"),
            #         temperature=options.get("temperature", 0),
            #         response_format="text"
            #     )
            # return response
            
            # Simulação de transcrição bem-sucedida
            simulated_result = f"[SIMULAÇÃO OpenAI] Transcrição do arquivo {audio_file.filename}"
            
            # Simula possível falha para testes
            if "fail" in audio_file.filename.lower():
                raise TranscriberException("Simulação de falha na API OpenAI")
            
            logger.info("Transcrição OpenAI completada com sucesso")
            return simulated_result
            
        except TranscriberException:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado na transcrição OpenAI: {str(e)}")
            raise TranscriberException(f"Erro na API OpenAI: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Verifica se a API OpenAI está disponível.
        
        Returns:
            True se disponível, False caso contrário
        """
        # Em produção, aqui seria feito um ping ou verificação real da API
        # Por enquanto, simula disponibilidade baseada na presença da API key
        return self.api_key is not None and len(self.api_key.strip()) > 0
    
    def get_name(self) -> str:
        """
        Retorna o nome identificador do transcriber.
        
        Returns:
            Nome do transcriber
        """
        return "openai"
    
    def supports_format(self, audio_format: str) -> bool:
        """
        Verifica se o formato de áudio é suportado.
        
        Args:
            audio_format: Formato do arquivo (mp3, wav, etc.)
            
        Returns:
            True se suportado, False caso contrário
        """
        # Normaliza o formato para incluir o ponto
        if not audio_format.startswith('.'):
            audio_format = f".{audio_format}"
        
        return audio_format.lower() in self._supported_formats
    
    def get_supported_formats(self) -> List[str]:
        """
        Retorna a lista de formatos suportados.
        
        Returns:
            Lista de extensões de arquivo suportadas
        """
        return self._supported_formats.copy()
