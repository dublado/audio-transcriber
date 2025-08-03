"""
Entidade TranscriptionJob.
Representa uma tarefa de transcrição de áudio.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from .audio_file import AudioFile


class TranscriptionStatus(Enum):
    """Status possíveis de uma tarefa de transcrição."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TranscriptionJob:
    """
    Entidade que representa uma tarefa de transcrição.
    
    Attributes:
        id: Identificador único da tarefa
        audio_file: Arquivo de áudio a ser transcrito
        status: Status atual da transcrição
        result: Texto transcrito (quando completado)
        error_message: Mensagem de erro (quando falhou)
        created_at: Data/hora de criação
        completed_at: Data/hora de conclusão
        transcriber_used: Nome do transcriber que foi usado
    """
    audio_file: AudioFile
    id: UUID = None
    status: TranscriptionStatus = TranscriptionStatus.PENDING
    result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    transcriber_used: Optional[str] = None
    
    def __post_init__(self):
        """Inicializa campos padrão se não fornecidos."""
        if self.id is None:
            object.__setattr__(self, 'id', uuid4())
        
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.now())
    
    def mark_in_progress(self, transcriber_name: str) -> None:
        """Marca a tarefa como em progresso."""
        self.status = TranscriptionStatus.IN_PROGRESS
        self.transcriber_used = transcriber_name
    
    def mark_completed(self, result: str) -> None:
        """Marca a tarefa como completada com sucesso."""
        self.status = TranscriptionStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now()
        self.error_message = None
    
    def mark_failed(self, error_message: str) -> None:
        """Marca a tarefa como falha."""
        self.status = TranscriptionStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()
        self.result = None
    
    @property
    def is_completed(self) -> bool:
        """Verifica se a transcrição foi completada com sucesso."""
        return self.status == TranscriptionStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """Verifica se a transcrição falhou."""
        return self.status == TranscriptionStatus.FAILED
    
    @property
    def is_finished(self) -> bool:
        """Verifica se a transcrição foi finalizada (sucesso ou falha)."""
        return self.status in [TranscriptionStatus.COMPLETED, TranscriptionStatus.FAILED]
