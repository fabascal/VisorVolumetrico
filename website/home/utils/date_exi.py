from datetime import datetime, date, timedelta

from datetime import datetime, date, timedelta

def FechaHora_minus_one_day(input_date):
    """
    Convert a date to a timestamp with specified hours, minutes, and seconds,
    after subtracting one day from the input date.
    
    Args:
    - input_date (date or str): A date object or date string in 'YYYY-MM-DD' format.

    Returns:
    - str: Formatted timestamp.
    """
    
    # Si input_date es una cadena de texto, conviértelo en una fecha
    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, '%Y-%m-%d').date()
    
    # Verifica si input_date es una instancia de date o datetime
    if isinstance(input_date, (date, datetime)):
        # Resta un día a la fecha
        adjusted_date = input_date - timedelta(days=1)
        # Convierte la fecha ajustada a formato de cadena y le agrega "T23:59:59"
        formatted_timestamp = adjusted_date.strftime('%Y-%m-%d') + "T23:59:59"
        return formatted_timestamp
    else:
        raise ValueError("input_date must be of type date, datetime, or a string in 'YYYY-MM-DD' format.")



def FechaHora(input_date):
    """
    Convert a date to a timestamp with specified hours, minutes, and seconds.
    
    Args:
    - input_date (date or str): A date object or date string in 'YYYY-MM-DD' format.

    Returns:
    - str: Formatted timestamp.
    """
    
    # Si input_date es una cadena de texto, conviértelo en una fecha
    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, '%Y-%m-%d').date()
    
    # Verifica si input_date es una instancia de date o datetime
    if isinstance(input_date, (date, datetime)):
        # Convierte la fecha a formato de cadena y le agrega "T23:59:59"
        formatted_timestamp = input_date.strftime('%Y-%m-%d') + "T23:59:59"
        return formatted_timestamp
    else:
        raise ValueError("input_date must be of type date, datetime, or a string in 'YYYY-MM-DD' format.")

