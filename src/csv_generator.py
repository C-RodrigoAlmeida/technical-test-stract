import csv
from typing import Any
from io import StringIO

def generate_csv(data: list[dict[str, Any]], headers: list[str]) -> str:
    """Generates a CSV in a table format with headers and rows using the csv module."""

    if not data:
        return "No data available"

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    
    writer.writeheader()
    for row in data:
        writer.writerow({header: row.get(header, "") for header in headers})
    
    return output.getvalue()