"""
Exemplo básico de uso do sistema de transcrição.
Demonstra como usar o pacote audio-transcriber de forma simples.
"""
import logging
from pathlib import Path

from audio_transcriber.domain.models.audio_file import AudioFile
from audio_transcriber.domain.models.transcription_job import TranscriptionJob
from audio_transcriber.domain.models.transcription_plan import TranscriptionPlan

from audio_transcriber.application.use_cases.execute_transcription_plan import ExecuteTranscriptionPlan
from audio_transcriber.application.policies.fallback_policy import (
    DefaultFallbackPolicy,
    AvailabilityFirstFallbackPolicy,
    FormatAwareFallbackPolicy
)

from audio_transcriber.infrastructure.transcribers.registry import TranscriberRegistry
from audio_transcriber.infrastructure.transcribers.openai_adapter import OpenAIAdapter
from audio_transcriber.infrastructure.transcribers.gemini_adapter import GeminiAdapter


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_transcribers() -> TranscriberRegistry:
    """
    Configura e registra todos os transcribers disponíveis.
    
    Returns:
        Registry configurado com todos os transcribers
    """
    registry = TranscriberRegistry()
    
    # Configuração do OpenAI (simula API key válida)
    openai_adapter = OpenAIAdapter(
        api_key="sk-fake-openai-key-for-simulation",
        model="whisper-1"
    )
    
    # Configuração do Gemini (simula credenciais válidas)
    gemini_adapter = GeminiAdapter(
        credentials_path="/path/to/credentials.json",
        project_id="my-gcp-project"
    )
    
    # Registra os transcribers
    registry.register(openai_adapter)
    registry.register(gemini_adapter)
    
    logger.info(f"Transcribers registrados: {registry.list_names()}")
    logger.info(f"Transcribers disponíveis: {registry.list_available()}")
    
    return registry


def create_sample_audio_file() -> AudioFile:
    """
    Cria um arquivo de áudio de exemplo para demonstração.
    
    Returns:
        AudioFile configurado para demonstração
    """
    # Cria um arquivo temporário de exemplo
    sample_path = Path("sample_audio.mp3")
    if not sample_path.exists():
        # Simula criação do arquivo
        sample_path.touch()
    
    return AudioFile(
        path=sample_path,
        format="mp3",
        duration_seconds=120.5,
        size_bytes=1024000
    )


def example_basic_transcription():
    """Exemplo básico de transcrição com um transcriber."""
    logger.info("=== Exemplo Básico de Transcrição ===")
    
    # Setup
    registry = setup_transcribers()
    fallback_policy = DefaultFallbackPolicy()
    use_case = ExecuteTranscriptionPlan(registry, fallback_policy)
    
    # Cria job e plano
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    plan = TranscriptionPlan.create_simple("openai")
    
    # Executa transcrição
    result = use_case.execute(job, plan)
    
    # Mostra resultado
    if result.is_completed:
        logger.info(f"✅ Transcrição completada: {result.result}")
        logger.info(f"📊 Transcriber usado: {result.transcriber_used}")
    else:
        logger.error(f"❌ Transcrição falhou: {result.error_message}")


def example_fallback_transcription():
    """Exemplo de transcrição com fallback."""
    logger.info("\n=== Exemplo com Fallback ===")
    
    # Setup
    registry = setup_transcribers()
    fallback_policy = DefaultFallbackPolicy()
    use_case = ExecuteTranscriptionPlan(registry, fallback_policy)
    
    # Cria job e plano com fallback
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["openai", "gemini"],
        max_retries=2
    )
    
    # Executa transcrição
    result = use_case.execute(job, plan)
    
    # Mostra resultado
    if result.is_completed:
        logger.info(f"✅ Transcrição completada: {result.result}")
        logger.info(f"📊 Transcriber usado: {result.transcriber_used}")
    else:
        logger.error(f"❌ Transcrição falhou: {result.error_message}")


def example_format_aware_policy():
    """Exemplo usando política que considera o formato do áudio."""
    logger.info("\n=== Exemplo com Política Format-Aware ===")
    
    # Setup
    registry = setup_transcribers()
    audio_file = create_sample_audio_file()
    
    # Usa política que considera o formato
    fallback_policy = FormatAwareFallbackPolicy(audio_file.format)
    use_case = ExecuteTranscriptionPlan(registry, fallback_policy)
    
    # Cria job e plano
    job = TranscriptionJob(audio_file=audio_file)
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["openai", "gemini"],
        options={
            "openai": {"language": "pt", "temperature": 0.1},
            "gemini": {"language_code": "pt-BR", "sample_rate_hertz": 16000}
        }
    )
    
    # Executa transcrição
    result = use_case.execute(job, plan)
    
    # Mostra resultado
    if result.is_completed:
        logger.info(f"✅ Transcrição completada: {result.result}")
        logger.info(f"📊 Transcriber usado: {result.transcriber_used}")
    else:
        logger.error(f"❌ Transcrição falhou: {result.error_message}")


def example_availability_first_policy():
    """Exemplo usando política que prioriza disponibilidade."""
    logger.info("\n=== Exemplo com Política Availability-First ===")
    
    # Setup
    registry = setup_transcribers()
    fallback_policy = AvailabilityFirstFallbackPolicy()
    use_case = ExecuteTranscriptionPlan(registry, fallback_policy)
    
    # Cria job e plano
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["gemini", "openai"],  # Ordem diferente para mostrar reordenação
        max_retries=1,
        timeout_seconds=60
    )
    
    # Executa transcrição
    result = use_case.execute(job, plan)
    
    # Mostra resultado
    if result.is_completed:
        logger.info(f"✅ Transcrição completada: {result.result}")
        logger.info(f"📊 Transcriber usado: {result.transcriber_used}")
    else:
        logger.error(f"❌ Transcrição falhou: {result.error_message}")


def cleanup():
    """Remove arquivos temporários criados para demonstração."""
    sample_path = Path("sample_audio.mp3")
    if sample_path.exists():
        sample_path.unlink()


def main():
    """Função principal que executa todos os exemplos."""
    logger.info("🚀 Iniciando demonstração do Sistema de Transcrição Agnóstico")
    
    try:
        # Executa exemplos
        example_basic_transcription()
        example_fallback_transcription()
        example_format_aware_policy()
        example_availability_first_policy()
        
        logger.info("\n✨ Demonstração concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro durante a demonstração: {str(e)}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
