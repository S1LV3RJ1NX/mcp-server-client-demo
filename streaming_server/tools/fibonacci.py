import asyncio
from datetime import datetime
from typing import Any, Dict

from streaming_server.tools import mcp_tool


@mcp_tool(name="calculate_fibonacci", description="Calculate fibonacci sequence")
async def calculate_fibonacci(n: int) -> Dict[str, Any]:
    """Calculate fibonacci sequence"""
    if n <= 0:
        return {"error": "n must be positive"}
    if n > 50:
        return {"error": "n too large (max 50)"}

    sequence = []
    a, b = 0, 1

    for i in range(n):
        sequence.append(a)
        a, b = b, a + b
        # Small delay to show async nature
        await asyncio.sleep(0.01)

    return {
        "sequence": sequence,
        "count": len(sequence),
        "last_number": sequence[-1] if sequence else 0,
        "largest_number": max(sequence) if sequence else 0,
        "golden_ratio_approximation": round(sequence[-1] / sequence[-2], 6)
        if len(sequence) > 1
        else 0,
        "calculated_at": datetime.now().isoformat(),
    }


@mcp_tool(name="fibonacci_stats", description="Get fibonacci statistics")
async def fibonacci_stats(max_number: int = 20) -> Dict[str, Any]:
    """Calculate fibonacci statistics"""
    if max_number <= 0:
        return {"error": "max_number must be positive"}
    if max_number > 50:
        return {"error": "max_number too large (max 50)"}

    fib_numbers = []
    a, b = 0, 1

    for i in range(max_number):
        fib_numbers.append(a)
        a, b = b, a + b
        await asyncio.sleep(0.01)

    # Calculate statistics
    total_sum = sum(fib_numbers)
    even_count = sum(1 for x in fib_numbers if x % 2 == 0)
    odd_count = len(fib_numbers) - even_count

    return {
        "sequence_length": len(fib_numbers),
        "complete_sequence": fib_numbers,
        "sum": total_sum,
        "average": round(total_sum / len(fib_numbers), 2),
        "even_count": even_count,
        "odd_count": odd_count,
        "largest_number": max(fib_numbers),
        "golden_ratio_approximation": round(fib_numbers[-1] / fib_numbers[-2], 6)
        if len(fib_numbers) > 1
        else 0,
        "calculated_at": datetime.now().isoformat(),
    }
