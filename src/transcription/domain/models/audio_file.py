"""
Objeto de valor AudioFile.
Representa dados sobre o arquivo de áudio a ser transcrito.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class AudioFile:
    """
    Objeto de valor que representa um arquivo de áudio.
    
    Attributes:
        path: Caminho para o arquivo de áudio
        format: Formato do arquivo (mp3, wav, etc.)
        duration_seconds: Duração em segundos (opcional)
        size_bytes: Tamanho em bytes (opcional)
    """
    path: Path
    format: str
    duration_seconds: Optional[float] = None
    size_bytes: Optional[int] = None
    
    def __post_init__(self):
        """Valida os dados do arquivo de áudio."""
        if not self.path.exists():
            raise ValueError(f"Arquivo de áudio não encontrado: {self.path}")
        
        if not self.format:
            raise ValueError("Formato do arquivo é obrigatório")
        
        if self.duration_seconds is not None and self.duration_seconds <= 0:
            raise ValueError("Duração deve ser positiva")
        
        if self.size_bytes is not None and self.size_bytes <= 0:
            raise ValueError("Tamanho deve ser positivo")
    
    @property
    def filename(self) -> str:
        """Retorna o nome do arquivo."""
        return self.path.name
    
    @property
    def extension(self) -> str:
        """Retorna a extensão do arquivo."""
        return self.path.suffix.lower()
