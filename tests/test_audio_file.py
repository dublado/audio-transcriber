"""
Testes para o modelo AudioFile.
"""
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from audio_transcriber.domain.models.audio_file import AudioFile


class TestAudioFile:
    """Testes para o objeto de valor AudioFile."""
    
    def test_create_valid_audio_file(self):
        """Testa criação de AudioFile válido."""
        with NamedTemporaryFile(suffix=".mp3") as temp_file:
            audio_file = AudioFile(
                path=Path(temp_file.name),
                format="mp3",
                duration_seconds=120.5,
                size_bytes=1024000
            )
            
            assert audio_file.path == Path(temp_file.name)
            assert audio_file.format == "mp3"
            assert audio_file.duration_seconds == 120.5
            assert audio_file.size_bytes == 1024000
    
    def test_file_not_exists_raises_error(self):
        """Testa que arquivo inexistente gera erro."""
        with pytest.raises(ValueError, match="Arquivo de áudio não encontrado"):
            AudioFile(
                path=Path("/caminho/inexistente.mp3"),
                format="mp3"
            )
    
    def test_empty_format_raises_error(self):
        """Testa que formato vazio gera erro."""
        with NamedTemporaryFile(suffix=".mp3") as temp_file:
            with pytest.raises(ValueError, match="Formato do arquivo é obrigatório"):
                AudioFile(
                    path=Path(temp_file.name),
                    format=""
                )
    
    def test_negative_duration_raises_error(self):
        """Testa que duração negativa gera erro."""
        with NamedTemporaryFile(suffix=".mp3") as temp_file:
            with pytest.raises(ValueError, match="Duração deve ser positiva"):
                AudioFile(
                    path=Path(temp_file.name),
                    format="mp3",
                    duration_seconds=-10
                )
    
    def test_negative_size_raises_error(self):
        """Testa que tamanho negativo gera erro."""
        with NamedTemporaryFile(suffix=".mp3") as temp_file:
            with pytest.raises(ValueError, match="Tamanho deve ser positivo"):
                AudioFile(
                    path=Path(temp_file.name),
                    format="mp3",
                    size_bytes=-100
                )
    
    def test_filename_property(self):
        """Testa propriedade filename."""
        with NamedTemporaryFile(suffix=".mp3") as temp_file:
            audio_file = AudioFile(
                path=Path(temp_file.name),
                format="mp3"
            )
            
            assert audio_file.filename == Path(temp_file.name).name
    
    def test_extension_property(self):
        """Testa propriedade extension."""
        with NamedTemporaryFile(suffix=".MP3") as temp_file:
            audio_file = AudioFile(
                path=Path(temp_file.name),
                format="mp3"
            )
            
            assert audio_file.extension == ".mp3"  # Deve ser lowercase
