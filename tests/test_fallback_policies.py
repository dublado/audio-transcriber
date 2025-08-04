"""
Testes para políticas de fallback.
"""
import pytest
from unittest.mock import Mock

from audio_transcriber.application.policies.fallback_policy import (
    DefaultFallbackPolicy,
    AvailabilityFirstFallbackPolicy,
    FormatAwareFallbackPolicy
)


class TestDefaultFallbackPolicy:
    """Testes para DefaultFallbackPolicy."""
    
    def test_resolve_available_transcribers(self):
        """Testa resolução de transcribers disponíveis."""
        policy = DefaultFallbackPolicy()
        
        # Mock registry
        registry = Mock()
        
        # Mock transcribers
        available_transcriber = Mock()
        available_transcriber.is_available.return_value = True
        
        unavailable_transcriber = Mock()
        unavailable_transcriber.is_available.return_value = False
        
        registry.get_transcriber.side_effect = lambda name: {
            "available": available_transcriber,
            "unavailable": unavailable_transcriber
        }.get(name)
        
        # Testa resolução
        result = policy.resolve(["available", "unavailable"], registry)
        
        assert len(result) == 1
        assert result[0] == available_transcriber
    
    def test_resolve_maintains_order(self):
        """Testa que a ordem é mantida."""
        policy = DefaultFallbackPolicy()
        
        # Mock registry
        registry = Mock()
        
        # Mock transcribers
        transcriber1 = Mock()
        transcriber1.is_available.return_value = True
        
        transcriber2 = Mock()
        transcriber2.is_available.return_value = True
        
        registry.get_transcriber.side_effect = lambda name: {
            "first": transcriber1,
            "second": transcriber2
        }.get(name)
        
        # Testa ordem
        result = policy.resolve(["second", "first"], registry)
        
        assert len(result) == 2
        assert result[0] == transcriber2  # Segundo foi listado primeiro
        assert result[1] == transcriber1


class TestAvailabilityFirstFallbackPolicy:
    """Testes para AvailabilityFirstFallbackPolicy."""
    
    def test_prioritizes_available_transcribers(self):
        """Testa que transcribers disponíveis são priorizados."""
        policy = AvailabilityFirstFallbackPolicy()
        
        # Mock registry
        registry = Mock()
        
        # Mock transcribers
        available_transcriber = Mock()
        available_transcriber.is_available.return_value = True
        
        unavailable_transcriber = Mock()
        unavailable_transcriber.is_available.return_value = False
        
        registry.get_transcriber.side_effect = lambda name: {
            "unavailable": unavailable_transcriber,
            "available": available_transcriber
        }.get(name)
        
        # Testa que disponível vem primeiro, mesmo sendo listado depois
        result = policy.resolve(["unavailable", "available"], registry)
        
        assert len(result) == 2
        assert result[0] == available_transcriber  # Disponível primeiro
        assert result[1] == unavailable_transcriber  # Indisponível depois


class TestFormatAwareFallbackPolicy:
    """Testes para FormatAwareFallbackPolicy."""
    
    def test_filters_by_format_support(self):
        """Testa filtragem por suporte a formato."""
        policy = FormatAwareFallbackPolicy("mp3")
        
        # Mock registry
        registry = Mock()
        
        # Mock transcribers
        mp3_transcriber = Mock()
        mp3_transcriber.is_available.return_value = True
        mp3_transcriber.supports_format.return_value = True
        
        wav_only_transcriber = Mock()
        wav_only_transcriber.is_available.return_value = True
        wav_only_transcriber.supports_format.return_value = False
        
        registry.get_transcriber.side_effect = lambda name: {
            "mp3_support": mp3_transcriber,
            "wav_only": wav_only_transcriber
        }.get(name)
        
        # Testa filtragem
        result = policy.resolve(["mp3_support", "wav_only"], registry)
        
        assert len(result) == 1
        assert result[0] == mp3_transcriber
        
        # Verifica se foi chamado com o formato correto
        mp3_transcriber.supports_format.assert_called_with("mp3")
        wav_only_transcriber.supports_format.assert_called_with("mp3")
