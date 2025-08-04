São Vicente - 04/08/2025

# Como Criei Meu Próprio Sistema de Transcrição de Áudio Open Source para o Telegram (e Nunca Mais Precisei Ouvir Áudios!)

## Motivação

Se você, como eu, já recebeu áudios intermináveis no Telegram, sabe o quanto pode ser cansativo ouvir tudo — especialmente quando a função de transcrição oficial é paga e exige assinatura anual. Como desenvolvedor, decidi que não queria depender de serviços pagos para algo tão simples. E mais: queria integrar a solução ao meu bot multi-agent do Telegram, tornando a experiência ainda mais prática e automatizada.

## O Problema

- Áudios do Telegram são cada vez mais comuns, mas a transcrição automática é um recurso restrito a assinantes.
- Ouvir áudios consome tempo e energia, principalmente em grupos ou canais profissionais.
- Soluções existentes são fechadas, pagas ou pouco flexíveis para integração com bots customizados.

## A Solução: Um Sistema de Transcrição Agnóstico e Extensível

Desenvolvi um sistema open source, com arquitetura hexagonal e Domain-Driven Design (DDD), capaz de integrar múltiplos provedores de IA (OpenAI, Gemini, etc.) sem acoplamento direto. O sistema é modular, testável e pronto para ser usado em qualquer projeto Python — inclusive bots do Telegram!

### Principais Características

- **Agnóstico a provedores de IA**: Você pode usar OpenAI, Gemini, ou adicionar qualquer outro backend facilmente.
- **Extensível**: Basta implementar a interface `Transcriber` para adicionar novos provedores.
- **Fallback automático**: Se um provedor falhar, o sistema tenta o próximo da lista.
- **Configuração flexível**: Permite definir idioma, timeout, número de tentativas e opções específicas por provedor.
- **Testes automatizados**: Cobertura completa para garantir robustez.
- **Pronto para bots**: Basta importar o pacote e integrar ao seu bot multi-agent.

## Como Funciona

1. **Recebe o áudio** do Telegram (ou de qualquer fonte).
2. **Cria uma tarefa de transcrição** (`TranscriptionJob`) com o arquivo recebido.
3. **Define um plano de transcrição** (`TranscriptionPlan`) com provedores e políticas de fallback.
4. **Executa o caso de uso** (`ExecuteTranscriptionPlan`), que orquestra a transcrição e retorna o texto.
5. **Entrega o resultado** para o usuário, sem precisar ouvir o áudio!

## O Que Aprendi

- **Arquitetura hexagonal** realmente facilita a manutenção e extensão do sistema.
- **Domain-Driven Design** ajuda a separar regras de negócio de detalhes técnicos.
- **Fallback inteligente** é essencial para garantir robustez em sistemas que dependem de APIs externas.
- **Open source é liberdade**: agora qualquer pessoa pode usar, adaptar e contribuir.
- **Bots multi-agent podem ser muito mais úteis** quando integrados a sistemas abertos e flexíveis.

## Resultado Final

- Nunca mais precisei ouvir áudios do Telegram — tudo é transcrito automaticamente!
- Não pago assinatura anual para um recurso simples.
- O sistema está disponível para qualquer pessoa usar, adaptar ou integrar em seus próprios projetos.
- Aprendi muito sobre arquitetura, testes e integração de IA.

## Como Usar

1. Clone o repositório: `git clone <url-do-repo>`
2. Instale as dependências: `pdm install -G dev`
3. Execute o exemplo: `python examples/simple_usage.py`
4. Integre ao seu bot multi-agent do Telegram!

## Próximo Desafio: Otimização de Custo e Velocidade

O próximo passo para evoluir o sistema será adicionar um filtro de otimização, acelerando o áudio antes de enviar para transcrição. A ideia é inspirada no artigo [OpenAI Charges by the Minute, So Make the Minutes Shorter](https://george.mand.is/2025/06/openai-charges-by-the-minute-so-make-the-minutes-shorter/), onde acelerar o áudio pode reduzir o tempo (e custo) de processamento, sem perder a inteligibilidade para os modelos de IA.

- **Por que acelerar?**
  - Provedores como OpenAI cobram por minuto de áudio processado.
  - Áudios acelerados podem ser transcritos mais rápido e com menor custo.
  - O filtro pode ser ajustado para manter a clareza da fala, mesmo em velocidades maiores.

- **Desafio extra:** Será que isso funcionaria com vídeos? 😄

Essa otimização pode ser integrada como uma etapa opcional no pipeline, tornando o sistema ainda mais eficiente e econômico para quem recebe muitos áudios (ou vídeos) diariamente.

## Tags

- transcrição de áudio
- telegram
- open source
- python
- inteligência artificial
- bots
- arquitetura hexagonal
- ddd
- automação
- multi-agent

## Prompt para Imagem

> "Ilustração de um bot do Telegram ouvindo áudios e transformando em texto automaticamente, com ícones de IA, código aberto e integração entre múltiplos provedores de inteligência artificial. Estilo moderno, cores azul e branco, visual limpo e tecnológico."

---

### Chamada LinkedIn
> "Se você, como eu, já recebeu áudios intermináveis no Telegram, sabe o quanto pode ser cansativo ouvir tudo — especialmente quando a função de transcrição oficial é paga e exige assinatura anual. Ofereci uma alternativa open source, só conferir."

**Se gostou do projeto, contribua ou compartilhe! Nunca mais ouça áudios — apenas leia!**
