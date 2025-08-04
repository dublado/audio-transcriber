"""
Caso de uso: ExecuteTranscriptionPlan.
Orquestra o processo de transcrição utilizando o plano especificado.
"""
import logging
from typing import TYPE_CHECKING

from ...domain.models.transcription_job import TranscriptionJob
from ...domain.models.transcription_plan import TranscriptionPlan
from ...domain.interfaces.transcriber import (
    Transcriber, 
    TranscriberException, 
    TranscriberTimeoutException,
    TranscriberUnavailableException
)

if TYPE_CHECKING:
    from ...infrastructure.transcribers.registry import TranscriberRegistry
    from ..policies.fallback_policy import FallbackPolicy


logger = logging.getLogger(__name__)


class ExecuteTranscriptionPlan:
    """
    Caso de uso responsável por executar um plano de transcrição.
    
    Orquestra todo o processo de transcrição, incluindo:
    - Resolução de transcribers através da política de fallback
    - Execução sequencial com retry
    - Tratamento de erros e fallbacks
    """
    
    def __init__(self, registry: 'TranscriberRegistry', fallback_policy: 'FallbackPolicy'):
        """
        Inicializa o caso de uso.
        
        Args:
            registry: Registry contendo os transcribers disponíveis
            fallback_policy: Política para resolver fallbacks
        """
        self.registry = registry
        self.fallback_policy = fallback_policy
    
    def execute(self, job: TranscriptionJob, plan: TranscriptionPlan) -> TranscriptionJob:
        """
        Executa o plano de transcrição.
        
        Args:
            job: Tarefa de transcrição a ser executada
            plan: Plano definindo a estratégia de transcrição
            
        Returns:
            A mesma tarefa atualizada com o resultado
            
        Raises:
            TranscriberException: Quando todos os transcribers falharam
        """
        logger.info(f"Iniciando execução do plano para job {job.id}")
        
        # Resolve os transcribers usando a política de fallback
        transcribers = self.fallback_policy.resolve(plan.transcriber_names, self.registry)
        
        if not transcribers:
            error_msg = f"Nenhum transcriber disponível para os nomes: {plan.transcriber_names}"
            logger.error(error_msg)
            job.mark_failed(error_msg)
            return job
        
        # Tenta cada transcriber sequencialmente
        last_error = None
        for transcriber in transcribers:
            try:
                logger.info(f"Tentando transcriber: {transcriber.get_name()}")
                result = self._try_transcriber(transcriber, job, plan)
                
                if result:
                    job.mark_completed(result)
                    logger.info(f"Transcrição completada com sucesso usando {transcriber.get_name()}")
                    return job
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Falha no transcriber {transcriber.get_name()}: {str(e)}")
                continue
        
        # Se chegou aqui, todos os transcribers falharam
        error_msg = f"Todos os transcribers falharam. Último erro: {str(last_error)}"
        logger.error(error_msg)
        job.mark_failed(error_msg)
        return job
    
    def _try_transcriber(self, transcriber: Transcriber, job: TranscriptionJob, plan: TranscriptionPlan) -> str:
        """
        Tenta executar a transcrição com um transcriber específico.
        
        Args:
            transcriber: Transcriber a ser usado
            job: Tarefa de transcrição
            plan: Plano de transcrição
            
        Returns:
            Texto transcrito se bem-sucedido
            
        Raises:
            TranscriberException: Se a transcrição falhar após todas as tentativas
        """
        job.mark_in_progress(transcriber.get_name())
        
        # Valida se o transcriber suporta o formato
        transcriber.validate_audio_file(job.audio_file)
        
        # Obtém opções específicas para este transcriber
        options = plan.get_transcriber_options(transcriber.get_name())
        
        # Tenta transcrever com retry
        last_exception = None
        for attempt in range(plan.max_retries):
            try:
                logger.debug(f"Tentativa {attempt + 1}/{plan.max_retries} para {transcriber.get_name()}")
                
                result = transcriber.transcribe(job.audio_file, options)
                
                if result and result.strip():
                    return result
                else:
                    raise TranscriberException("Transcrição retornou resultado vazio")
                    
            except (TranscriberTimeoutException, TranscriberUnavailableException) as e:
                # Erros que não devem ser retentados
                logger.warning(f"Erro não recuperável no transcriber {transcriber.get_name()}: {str(e)}")
                raise e
                
            except TranscriberException as e:
                last_exception = e
                logger.debug(f"Tentativa {attempt + 1} falhou: {str(e)}")
                
                # Se não é a última tentativa, continua
                if attempt < plan.max_retries - 1:
                    continue
                else:
                    # Última tentativa falhou
                    break
        
        # Se chegou aqui, todas as tentativas falharam
        if last_exception:
            raise last_exception
        else:
            raise TranscriberException(f"Transcriber {transcriber.get_name()} falhou após {plan.max_retries} tentativas")
