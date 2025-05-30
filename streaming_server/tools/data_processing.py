import asyncio
import random
from datetime import datetime
from typing import Any, Dict, List

from streaming_server.tools import mcp_tool


@mcp_tool(name="process_large_dataset", description="Process large dataset")
async def process_large_dataset(
    size: int = 100, processing_delay: float = 0.01
) -> Dict[str, Any]:
    """Process large dataset with simple async processing"""
    if size <= 0:
        return {"error": "Size must be positive"}
    if size > 1000:
        return {"error": "Size too large (max 1000)"}
    if processing_delay < 0:
        return {"error": "Processing delay must be non-negative"}

    results = []

    for i in range(size):
        # Simulate processing time
        await asyncio.sleep(processing_delay)

        # Generate random data point
        value = random.randint(1, 1000)
        result_item = {
            "id": i,
            "value": value,
            "squared": value * value,
            "processed_at": datetime.now().isoformat(),
        }
        results.append(result_item)

    # Calculate final statistics
    values = [r["value"] for r in results]

    return {
        "total_processed": len(results),
        "sample_results": results[:5],  # First 5 for brevity
        "summary": {
            "min_value": min(values),
            "max_value": max(values),
            "avg_value": round(sum(values) / len(values), 2),
            "total_sum": sum(values),
        },
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "batch_size": size,
            "processing_time_per_item": processing_delay,
        },
    }


@mcp_tool(name="analyze_logs", description="Analyze log data")
async def analyze_logs(log_lines: int = 500, error_rate: float = 0.1) -> Dict[str, Any]:
    """Analyze log data with simple processing"""
    if log_lines <= 0:
        return {"error": "log_lines must be positive"}
    if log_lines > 5000:
        return {"error": "log_lines too large (max 5000)"}
    if not 0 <= error_rate <= 1:
        return {"error": "error_rate must be between 0 and 1"}

    log_levels = ["INFO", "DEBUG", "WARN", "ERROR", "FATAL"]
    level_counts = {level: 0 for level in log_levels}
    error_messages = []

    for i in range(log_lines):
        # Simulate processing delay
        await asyncio.sleep(0.001)

        # Generate log entry
        if random.random() < error_rate:
            level = random.choice(["ERROR", "FATAL"])
            if level == "ERROR":
                error_msg = f"Error on line {i + 1}: {random.choice(['Database connection failed', 'File not found', 'Permission denied', 'Timeout occurred'])}"
                error_messages.append(error_msg)
        else:
            level = random.choice(["INFO", "DEBUG", "WARN"])

        level_counts[level] += 1

    # Final analysis results
    total_errors = level_counts["ERROR"] + level_counts["FATAL"]
    final_error_percentage = (total_errors / log_lines) * 100

    return {
        "total_lines_analyzed": log_lines,
        "log_level_distribution": level_counts,
        "error_statistics": {
            "total_errors": total_errors,
            "error_percentage": round(final_error_percentage, 2),
            "target_error_rate": round(error_rate * 100, 2),
            "variance_from_target": round(
                abs(final_error_percentage - (error_rate * 100)), 2
            ),
        },
        "sample_errors": error_messages[:5],  # First 5 errors
        "analysis_completed_at": datetime.now().isoformat(),
    }


@mcp_tool(name="get_current_time", description="Get current timestamp")
async def get_current_time() -> str:
    """Get the current timestamp"""
    return f"Current time: {datetime.now().isoformat()}"
