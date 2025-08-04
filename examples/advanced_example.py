"""
Exemplo avançado de uso do sistema de transcrição.
Demonstra políticas personalizadas e configurações avançadas.
"""
import logging
from pathlib import Path

# Importações do pacote audio_transcriber
from audio_transcriber.domain.models.audio_file import AudioFile
from audio_transcriber.domain.models.transcription_job import TranscriptionJob
from audio_transcriber.domain.models.transcription_plan import TranscriptionPlan
from audio_transcriber.infrastructure.transcribers.registry import TranscriberRegistry
from audio_transcriber.infrastructure.transcribers.openai_adapter import OpenAIAdapter
from audio_transcriber.infrastructure.transcribers.gemini_adapter import GeminiAdapter
from audio_transcriber.application.use_cases.execute_transcription_plan import ExecuteTranscriptionPlan
from audio_transcriber.application.policies.fallback_policy import (
    DefaultFallbackPolicy,
    AvailabilityFirstFallbackPolicy,
    FormatAwareFallbackPolicy
)


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_audio_file() -> AudioFile:
    """Cria um arquivo de áudio de exemplo."""
    sample_path = Path("sample_advanced.mp3")
    if not sample_path.exists():
        sample_path.touch()
    
    return AudioFile(
        path=sample_path,
        format="mp3",
        duration_seconds=300.0,
        size_bytes=3072000
    )


def setup_registry() -> TranscriberRegistry:
    """Configura o registry com todos os provedores."""
    registry = TranscriberRegistry()
    
    # Configuração com opções específicas por provedor
    openai_adapter = OpenAIAdapter(
        api_key="sk-fake-openai-key-for-demo",
        model="whisper-1"
    )
    
    gemini_adapter = GeminiAdapter(
        credentials_path="/path/to/credentials.json",
        project_id="my-gcp-project"
    )
    
    registry.register(openai_adapter)
    registry.register(gemini_adapter)
    
    return registry


def example_with_availability_first_policy():
    """Exemplo usando política que prioriza disponibilidade."""
    print("\n🎯 Exemplo: Política Availability-First")
    print("=" * 50)
    
    registry = setup_registry()
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    
    # Plano com ordem específica, mas a política pode reordenar
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["gemini", "openai"],  # Gemini primeiro
        max_retries=2,
        timeout_seconds=120
    )
    
    # Política que prioriza disponibilidade sobre ordem
    policy = AvailabilityFirstFallbackPolicy()
    use_case = ExecuteTranscriptionPlan(registry, policy)
    
    result = use_case.execute(job, plan)
    
    if result.is_completed:
        print(f"✅ Sucesso: {result.result}")
        print(f"📊 Provedor usado: {result.transcriber_used}")
    else:
        print(f"❌ Falha: {result.error_message}")


def example_with_format_aware_policy():
    """Exemplo usando política que considera formato do áudio."""
    print("\n🎵 Exemplo: Política Format-Aware")
    print("=" * 50)
    
    registry = setup_registry()
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    
    # Plano com configurações específicas por provedor
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["openai", "gemini"],
        options={
            "openai": {
                "language": "pt",
                "temperature": 0.1,
                "response_format": "text"
            },
            "gemini": {
                "language_code": "pt-BR",
                "sample_rate_hertz": 16000,
                "encoding": "MP3"
            }
        }
    )
    
    # Política que filtra por formato suportado
    policy = FormatAwareFallbackPolicy(audio_file.format)
    use_case = ExecuteTranscriptionPlan(registry, policy)
    
    result = use_case.execute(job, plan)
    
    if result.is_completed:
        print(f"✅ Sucesso: {result.result}")
        print(f"📊 Provedor usado: {result.transcriber_used}")
    else:
        print(f"❌ Falha: {result.error_message}")


def example_with_custom_configuration():
    """Exemplo com configuração personalizada avançada."""
    print("\n⚙️ Exemplo: Configuração Personalizada")
    print("=" * 50)
    
    registry = setup_registry()
    audio_file = create_sample_audio_file()
    job = TranscriptionJob(audio_file=audio_file)
    
    # Plano complexo com múltiplas tentativas e timeout alto
    plan = TranscriptionPlan(
        transcriber_names=["openai", "gemini"],
        max_retries=3,
        timeout_seconds=300,
        options={
            "openai": {
                "language": "pt-BR",
                "temperature": 0.0,  # Máxima precisão
                "response_format": "verbose_json"
            },
            "gemini": {
                "language_code": "pt-BR",
                "enable_automatic_punctuation": True,
                "enable_word_time_offsets": True
            }
        }
    )
    
    policy = DefaultFallbackPolicy()
    use_case = ExecuteTranscriptionPlan(registry, policy)
    
    print(f"🎯 Plano: {plan.transcriber_names}")
    print(f"🔄 Max retries: {plan.max_retries}")
    print(f"⏱️ Timeout: {plan.timeout_seconds}s")
    
    result = use_case.execute(job, plan)
    
    if result.is_completed:
        print(f"\n✅ Transcrição completada!")
        print(f"📊 Provedor: {result.transcriber_used}")
        print(f"📝 Resultado: {result.result}")
        print(f"🕐 Status: {result.status.value}")
    else:
        print(f"\n❌ Transcrição falhou!")
        print(f"💥 Erro: {result.error_message}")
        print(f"🕐 Status: {result.status.value}")


def cleanup():
    """Remove arquivos temporários."""
    sample_path = Path("sample_advanced.mp3")
    if sample_path.exists():
        sample_path.unlink()


def main():
    """Executa todos os exemplos avançados."""
    print("🚀 Exemplos Avançados do Sistema de Transcrição")
    print("=" * 60)
    
    try:
        example_with_availability_first_policy()
        example_with_format_aware_policy()
        example_with_custom_configuration()
        
        print("\n✨ Todos os exemplos concluídos!")
        
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
