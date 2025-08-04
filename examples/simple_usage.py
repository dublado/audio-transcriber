"""
Exemplo simples de uso do pacote audio-transcriber.
Este exemplo mostra como usar o pacote instalado via pip.
"""
from pathlib import Path

# Após instalar o pacote com: pip install audio-transcriber
from audio_transcriber.domain.models.audio_file import AudioFile
from audio_transcriber.domain.models.transcription_job import TranscriptionJob
from audio_transcriber.domain.models.transcription_plan import TranscriptionPlan
from audio_transcriber.infrastructure.transcribers.registry import TranscriberRegistry
from audio_transcriber.infrastructure.transcribers.openai_adapter import OpenAIAdapter
from audio_transcriber.infrastructure.transcribers.gemini_adapter import GeminiAdapter
from audio_transcriber.application.use_cases.execute_transcription_plan import ExecuteTranscriptionPlan
from audio_transcriber.application.policies.fallback_policy import DefaultFallbackPolicy


def simple_transcription_example():
    """Exemplo básico de transcrição de áudio."""
    
    print("🎙️ Exemplo Simples de Transcrição de Áudio")
    print("=" * 50)
    
    # 1. Configurar o sistema
    print("\n1️⃣ Configurando o sistema...")
    registry = TranscriberRegistry()
    
    # Registrar provedores (substitua pelas suas chaves reais)
    openai_adapter = OpenAIAdapter(api_key="sua-chave-openai-aqui")
    gemini_adapter = GeminiAdapter(
        credentials_path="/path/to/credentials.json",
        project_id="seu-projeto-gcp"
    )
    
    registry.register(openai_adapter)
    registry.register(gemini_adapter)
    
    print(f"✅ Provedores registrados: {registry.list_names()}")
    
    # 2. Preparar arquivo de áudio
    print("\n2️⃣ Preparando arquivo de áudio...")
    
    # Crie um arquivo de áudio de exemplo (substitua pelo seu arquivo real)
    audio_path = Path("meu_audio.mp3")
    if not audio_path.exists():
        audio_path.touch()  # Simula criação do arquivo
    
    audio_file = AudioFile(
        path=audio_path,
        format="mp3",
        duration_seconds=120.0,
        size_bytes=1024000
    )
    
    print(f"📁 Arquivo: {audio_file.filename}")
    print(f"⏱️  Duração: {audio_file.duration_seconds}s")
    
    # 3. Criar tarefa de transcrição
    print("\n3️⃣ Criando tarefa de transcrição...")
    job = TranscriptionJob(audio_file=audio_file)
    
    # 4. Definir plano com fallback
    print("\n4️⃣ Definindo plano de transcrição...")
    plan = TranscriptionPlan.create_with_multiple_fallbacks(
        transcribers=["openai", "gemini"],  # Tenta OpenAI primeiro, depois Gemini
        max_retries=2,
        timeout_seconds=300
    )
    
    print(f"🎯 Ordem dos provedores: {plan.transcriber_names}")
    
    # 5. Executar transcrição
    print("\n5️⃣ Executando transcrição...")
    use_case = ExecuteTranscriptionPlan(
        registry=registry,
        fallback_policy=DefaultFallbackPolicy()
    )
    
    try:
        result = use_case.execute(job, plan)
        
        print("\n🎉 Transcrição concluída!")
        print(f"✅ Status: {result.status.value}")
        print(f"🤖 Provedor usado: {result.transcriber_used}")
        print(f"📝 Texto transcrito: {result.result}")
        
    except Exception as e:
        print(f"\n❌ Erro na transcrição: {e}")
    
    finally:
        # Limpar arquivo de exemplo
        if audio_path.exists():
            audio_path.unlink()


def main():
    """Função principal do exemplo."""
    simple_transcription_example()


if __name__ == "__main__":
    main()
