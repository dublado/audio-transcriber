# Exemplos de Uso do audio-transcriber

Esta pasta contém exemplos práticos de como usar o pacote `audio-transcriber`.

## 📁 Arquivos de Exemplo

### 1. `simple_usage.py` - Uso Básico 🚀
Exemplo mais simples e direto de como usar o pacote após instalação:

```bash
python examples/simple_usage.py
```

**O que demonstra:**
- Como instalar e importar o pacote
- Configuração básica com provedores
- Transcrição com fallback automático
- Tratamento de erros

### 2. `basic_example.py` - Exemplo Completo 🔧
Demonstração completa com todas as funcionalidades:

```bash
python examples/basic_example.py
```

**O que demonstra:**
- Múltiplos exemplos de uso
- Diferentes políticas de fallback
- Configurações avançadas
- Logging detalhado

### 3. `advanced_example.py` - Uso Avançado ⚡
Exemplos avançados com personalizações:

```bash
python examples/advanced_example.py
```

**O que demonstra:**
- Políticas personalizadas de fallback
- Configurações específicas por provedor
- Integração com sistemas externos

## 🚀 Como Usar em Seu Projeto

### 1. Instalação
```bash
pip install git+https://github.com/dublado/audio-transcriber.git
```

### 2. Uso Básico
```python
from audio_transcriber.domain.models.audio_file import AudioFile
from audio_transcriber.infrastructure.transcribers.registry import TranscriberRegistry
from audio_transcriber.infrastructure.transcribers.openai_adapter import OpenAIAdapter

# Configurar
registry = TranscriberRegistry()
registry.register(OpenAIAdapter(api_key="sua-chave"))

# Transcrever
audio = AudioFile(path="audio.mp3", format="mp3")
# ... resto da lógica
```

### 3. Com Fallback
```python
from audio_transcriber.domain.models.transcription_plan import TranscriptionPlan

plan = TranscriptionPlan.create_with_multiple_fallbacks(
    transcribers=["openai", "gemini"]
)
```

## 🔧 Configuração dos Provedores

### OpenAI
```python
from audio_transcriber.infrastructure.transcribers.openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter(
    api_key="sk-sua-chave-aqui",
    model="whisper-1"
)
```

### Google Gemini
```python
from audio_transcriber.infrastructure.transcribers.gemini_adapter import GeminiAdapter

adapter = GeminiAdapter(
    credentials_path="/path/to/credentials.json",
    project_id="seu-projeto-gcp"
)
```

## 📝 Notas Importantes

- **Chaves de API**: Substitua as chaves de exemplo pelas suas chaves reais
- **Arquivos de Áudio**: Use arquivos reais nos formatos suportados (mp3, wav, etc.)
- **Credenciais**: Mantenha suas credenciais seguras (use variáveis de ambiente)

## 🆘 Troubleshooting

### Erro de Importação
```bash
ModuleNotFoundError: No module named 'audio_transcriber'
```
**Solução**: Certifique-se de que o pacote foi instalado corretamente

### Erro de Dependências
```bash
pdm install -G dev
```

### Problemas com Testes
```bash
pdm run pytest tests/ -v
```
