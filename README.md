# Sistema de Transcrição de Áudio Agnóstico

Sistema de transcrição de áudio com arquitetura hexagonal e Domain-Driven Design (DDD), agnóstico a provedores de IA.

## 🏗️ Arquitetura

O sistema implementa **Arquitetura Hexagonal (Ports & Adapters)** com **Domain-Driven Design**, garantindo:

- **Desacoplamento**: O domínio não depende de infraestrutura externa
- **Extensibilidade**: Novos provedores podem ser adicionados facilmente
- **Testabilidade**: Componentes podem ser testados isoladamente
- **Flexibilidade**: Políticas de fallback intercambiáveis

### Estrutura de Camadas

```
src/transcription/
├── domain/                 # 🏛️ Camada de Domínio
│   ├── models/            # Entidades e Objetos de Valor
│   │   ├── audio_file.py           # AudioFile (Value Object)
│   │   ├── transcription_job.py    # TranscriptionJob (Entity)
│   │   └── transcription_plan.py   # TranscriptionPlan (Value Object)
│   └── interfaces/        # Contratos do Domínio
│       └── transcriber.py          # Interface Transcriber
│
├── application/           # 🔄 Camada de Aplicação
│   ├── use_cases/        # Casos de Uso
│   │   └── execute_transcription_plan.py
│   └── policies/         # Políticas de Negócio
│       └── fallback_policy.py
│
└── infrastructure/       # 🔧 Camada de Infraestrutura
    └── transcribers/     # Adaptadores de Saída
        ├── registry.py            # Service Locator
        ├── openai_adapter.py      # Adaptador OpenAI
        └── gemini_adapter.py      # Adaptador Google Gemini
```

## 🎯 Padrões de Projeto Utilizados

| Padrão | Aplicação | Problema Resolvido |
|--------|-----------|-------------------|
| **Strategy** | `FallbackPolicy` | Permite trocar dinamicamente como a IA é escolhida |
| **Service Locator** | `TranscriberRegistry` | Fornece instâncias de transcribers em tempo de execução |
| **Interface/Polimorfismo** | `Transcriber` | Abstrai múltiplos backends IA de forma uniforme |
| **Factory** | Métodos de criação em `TranscriptionPlan` | Flexibilidade na criação de objetos |
| **Hexagonal** | Arquitetura geral | Isola o domínio de dependências externas |

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.11+
- PDM (Python Development Master)

### Instalação

```bash
# Clone o repositório
git clone <url-do-repo>
cd audio-transcriber

# Instale dependências com PDM
pdm install

# Execute o exemplo
pdm run python main.py
```

### Uso Básico

```python
from pathlib import Path
from src.transcription.domain.models.audio_file import AudioFile
from src.transcription.domain.models.transcription_job import TranscriptionJob
from src.transcription.domain.models.transcription_plan import TranscriptionPlan
from src.transcription.application.use_cases.execute_transcription_plan import ExecuteTranscriptionPlan
from src.transcription.application.policies.fallback_policy import DefaultFallbackPolicy
from src.transcription.infrastructure.transcribers.registry import TranscriberRegistry
from src.transcription.infrastructure.transcribers.openai_adapter import OpenAIAdapter

# Setup
registry = TranscriberRegistry()
registry.register(OpenAIAdapter(api_key="sua-api-key"))

# Transcrição
audio_file = AudioFile(path=Path("audio.mp3"), format="mp3")
job = TranscriptionJob(audio_file=audio_file)
plan = TranscriptionPlan.create_simple("openai")

use_case = ExecuteTranscriptionPlan(registry, DefaultFallbackPolicy())
result = use_case.execute(job, plan)

print(result.result)  # Texto transcrito
```

## 🔄 Estratégias de Fallback

### DefaultFallbackPolicy
Usa transcribers na ordem especificada, apenas os disponíveis:

```python
plan = TranscriptionPlan.create_with_multiple_fallbacks(["openai", "gemini"])
policy = DefaultFallbackPolicy()
```

### AvailabilityFirstFallbackPolicy
Prioriza transcribers disponíveis, independente da ordem:

```python
policy = AvailabilityFirstFallbackPolicy()
```

### FormatAwareFallbackPolicy
Filtra apenas transcribers que suportam o formato do áudio:

```python
policy = FormatAwareFallbackPolicy("mp3")
```

## 🧩 Extensibilidade

### Adicionando Novo Provedor

1. **Implemente a interface Transcriber**:

```python
from src.transcription.domain.interfaces.transcriber import Transcriber

class NovoProviderAdapter(Transcriber):
    def transcribe(self, audio_file, options=None):
        # Implementação específica
        pass
    
    def is_available(self):
        # Verificação de disponibilidade
        pass
    
    def get_name(self):
        return "novo_provider"
    
    def supports_format(self, audio_format):
        # Verificação de formato suportado
        pass
```

2. **Registre no sistema**:

```python
registry.register(NovoProviderAdapter())
```

### Criando Nova Política de Fallback

```python
from src.transcription.application.policies.fallback_policy import FallbackPolicy

class MinhaPolicy(FallbackPolicy):
    def resolve(self, transcriber_names, registry):
        # Lógica personalizada de seleção
        pass
```

## 🎛️ Configurações Avançadas

### Opções por Transcriber

```python
plan = TranscriptionPlan.create_with_multiple_fallbacks(
    transcribers=["openai", "gemini"],
    options={
        "openai": {"language": "pt", "temperature": 0.1},
        "gemini": {"language_code": "pt-BR", "sample_rate_hertz": 16000}
    }
)
```

### Retry e Timeout

```python
plan = TranscriptionPlan(
    transcriber_names=["openai"],
    max_retries=3,
    timeout_seconds=120
)
```

## 🧪 Testes

```bash
# Execute os testes
pdm run pytest tests/

# Com cobertura
pdm run pytest tests/ --cov=src
```

## 📊 Status da Transcrição

O sistema rastreia o estado de cada transcrição:

- `PENDING`: Aguardando processamento
- `IN_PROGRESS`: Em andamento
- `COMPLETED`: Completada com sucesso
- `FAILED`: Falhou

```python
if job.is_completed:
    print(f"Sucesso: {job.result}")
elif job.is_failed:
    print(f"Erro: {job.error_message}")
```

## 🔍 Logs e Debugging

O sistema inclui logging detalhado:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido com 🏗️ Arquitetura Hexagonal e ❤️ Domain-Driven Design**