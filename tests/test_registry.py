"""
Testes para TranscriberRegistry.
"""
import pytest
from unittest.mock import Mock

from src.transcription.infrastructure.transcribers.registry import TranscriberRegistry
from src.transcription.domain.interfaces.transcriber import Transcriber


class MockTranscriber(Transcriber):
    """Mock transcriber para testes."""
    
    def __init__(self, name: str, available: bool = True):
        self._name = name
        self._available = available
    
    def transcribe(self, audio_file, options=None):
        return f"Transcrição mock de {self._name}"
    
    def is_available(self):
        return self._available
    
    def get_name(self):
        return self._name
    
    def supports_format(self, audio_format):
        return True


class TestTranscriberRegistry:
    """Testes para TranscriberRegistry."""
    
    def test_register_transcriber(self):
        """Testa registro de transcriber."""
        registry = TranscriberRegistry()
        transcriber = MockTranscriber("test")
        
        registry.register(transcriber)
        
        assert registry.has_transcriber("test")
        assert registry.get_transcriber("test") == transcriber
    
    def test_register_duplicate_name_raises_error(self):
        """Testa que registrar nome duplicado gera erro."""
        registry = TranscriberRegistry()
        transcriber1 = MockTranscriber("test")
        transcriber2 = MockTranscriber("test")
        
        registry.register(transcriber1)
        
        with pytest.raises(ValueError, match="Transcriber 'test' já está registrado"):
            registry.register(transcriber2)
    
    def test_unregister_transcriber(self):
        """Testa remoção de transcriber."""
        registry = TranscriberRegistry()
        transcriber = MockTranscriber("test")
        
        registry.register(transcriber)
        result = registry.unregister("test")
        
        assert result is True
        assert not registry.has_transcriber("test")
    
    def test_unregister_nonexistent_returns_false(self):
        """Testa remoção de transcriber inexistente."""
        registry = TranscriberRegistry()
        
        result = registry.unregister("inexistente")
        
        assert result is False
    
    def test_get_nonexistent_transcriber_returns_none(self):
        """Testa obtenção de transcriber inexistente."""
        registry = TranscriberRegistry()
        
        result = registry.get_transcriber("inexistente")
        
        assert result is None
    
    def test_list_names(self):
        """Testa listagem de nomes."""
        registry = TranscriberRegistry()
        transcriber1 = MockTranscriber("test1")
        transcriber2 = MockTranscriber("test2")
        
        registry.register(transcriber1)
        registry.register(transcriber2)
        
        names = registry.list_names()
        
        assert set(names) == {"test1", "test2"}
    
    def test_list_available(self):
        """Testa listagem de transcribers disponíveis."""
        registry = TranscriberRegistry()
        available_transcriber = MockTranscriber("available", available=True)
        unavailable_transcriber = MockTranscriber("unavailable", available=False)
        
        registry.register(available_transcriber)
        registry.register(unavailable_transcriber)
        
        available = registry.list_available()
        
        assert available == ["available"]
    
    def test_clear(self):
        """Testa limpeza do registry."""
        registry = TranscriberRegistry()
        transcriber = MockTranscriber("test")
        
        registry.register(transcriber)
        registry.clear()
        
        assert registry.count() == 0
        assert not registry.has_transcriber("test")
    
    def test_count(self):
        """Testa contagem de transcribers."""
        registry = TranscriberRegistry()
        
        assert registry.count() == 0
        
        registry.register(MockTranscriber("test1"))
        assert registry.count() == 1
        
        registry.register(MockTranscriber("test2"))
        assert registry.count() == 2
    
    def test_get_transcribers_for_format(self):
        """Testa obtenção de transcribers por formato."""
        registry = TranscriberRegistry()
        
        # Mock que suporta apenas mp3
        mp3_transcriber = Mock()
        mp3_transcriber.supports_format.side_effect = lambda fmt: fmt == "mp3"
        mp3_transcriber.get_name.return_value = "mp3_only"
        
        # Mock que suporta qualquer formato
        universal_transcriber = Mock()
        universal_transcriber.supports_format.return_value = True
        universal_transcriber.get_name.return_value = "universal"
        
        registry.register(mp3_transcriber)
        registry.register(universal_transcriber)
        
        mp3_compatible = registry.get_transcribers_for_format("mp3")
        wav_compatible = registry.get_transcribers_for_format("wav")
        
        assert len(mp3_compatible) == 2  # Ambos suportam mp3
        assert len(wav_compatible) == 1  # Apenas universal suporta wav
