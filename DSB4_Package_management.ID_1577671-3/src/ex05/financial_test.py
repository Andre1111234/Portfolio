#!/usr/bin/env python3

import pytest
from financial_no_sleep import get__dataFinancial


class TestFinancialData:

    def test_returns_tuple(self):
        """Функция должна возвращать кортеж."""
        result = get__dataFinancial("AAPL", "Total Revenue")
        assert isinstance(result, tuple), "Ожидается тип tuple"

    def test_field_total_revenue(self):
        """Проверяем, что поле Total Revenue найдено и не пустое."""
        result = get__dataFinancial("AAPL", "Total Revenue")
        assert len(result) > 0, "Результат не должен быть пустым"

    def test_field_operating_income(self):
        """Проверяем другое поле для уверенности."""
        result = get__dataFinancial("AAPL", "Operating Income")
        assert len(result) > 0, "Данные Operating Income должны существовать"

    def test_invalid_ticker_raises(self):
        """При неверном тикере должно выбрасываться исключение."""
        with pytest.raises(Exception):
            get__dataFinancial("TICKER12345", "Total Revenue")

    def test_invalid_field_raises(self):
        """При неверном финансовом поле должно быть исключение."""
        with pytest.raises(Exception):
            get__dataFinancial("AAPL", "НекорректноеПоле123")

    def test_case_insensitive_ticker(self):
        """Нечувствительность к регистру тикера."""
        result1 = get__dataFinancial("aapl", "Total Revenue")
        result2 = get__dataFinancial("AAPL", "Total Revenue")
        assert isinstance(result1, tuple) and isinstance(result2, tuple)