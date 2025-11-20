"""
Template filters para préstamos.
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Formatea un valor numérico como moneda.
    Ejemplo: 1234567.89 -> $1,234,567.89
    """
    if value is None:
        return '$0.00'
    
    try:
        # Convertir a Decimal si es necesario
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, (Decimal, int, float)):
            return '$0.00'
        
        # Formatear con separador de miles
        formatted = f"{value:,.2f}"
        return f"${formatted}"
    except (ValueError, TypeError):
        return '$0.00'


@register.filter(name='percentage')
def percentage(value):
    """
    Formatea un valor como porcentaje.
    Ejemplo: 15.5 -> 15.5%
    """
    if value is None:
        return '0%'
    
    try:
        if isinstance(value, str):
            value = float(value)
        return f"{value:.2f}%"
    except (ValueError, TypeError):
        return '0%'
