"""Tests for circuit breaker."""

import pytest
from src.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_initial_state():
    """Test circuit breaker initial state."""
    cb = CircuitBreaker(name="test")
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_success():
    """Test circuit breaker with successful call."""
    cb = CircuitBreaker(name="test", failure_threshold=3)

    def success_func():
        return "success"

    result = cb.call(success_func)
    assert result == "success"
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


def test_circuit_breaker_failure():
    """Test circuit breaker with failures."""
    cb = CircuitBreaker(name="test", failure_threshold=2)

    def failing_func():
        raise ValueError("Test error")

    # First failure
    with pytest.raises(ValueError):
        cb.call(failing_func)
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 1

    # Second failure - should open circuit
    with pytest.raises(ValueError):
        cb.call(failing_func)
    assert cb.state == CircuitState.OPEN
    assert cb.failure_count == 2


def test_circuit_breaker_open_state():
    """Test circuit breaker in open state."""
    cb = CircuitBreaker(name="test", failure_threshold=1, timeout=1)
    cb.state = CircuitState.OPEN

    def func():
        return "success"

    # Should raise exception when circuit is open
    with pytest.raises(Exception) as exc_info:
        cb.call(func)
    assert "OPEN" in str(exc_info.value)


def test_circuit_breaker_reset():
    """Test manual circuit breaker reset."""
    cb = CircuitBreaker(name="test")
    cb.state = CircuitState.OPEN
    cb.failure_count = 5

    cb.reset()
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0

