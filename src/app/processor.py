"""Processor module for insider trading and institutional ownership data."""

from typing import Any

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def process_insider_data(data: dict[str, Any]) -> dict[str, Any]:
    """Processes insider trading or institutional ownership data.

    Args:
        data (dict[str, Any]): Input data containing insider trade or holding information.

    Returns:
        dict[str, Any]: The enriched and validated data with standard fields.

    Notes:
        This processor can be extended to flag unusual trading patterns, 
        summarize ownership changes, or correlate with price movements.
    """
    try:
        # Normalize trade type
        trade_type = data.get("trade_type", "").strip().lower()
        if trade_type in {"buy", "purchase"}:
            data["normalized_action"] = "buy"
        elif trade_type in {"sell", "sale"}:
            data["normalized_action"] = "sell"
        else:
            data["normalized_action"] = "unknown"

        # Parse and validate number of shares
        try:
            data["shares"] = int(data.get("shares", 0))
        except (ValueError, TypeError):
            logger.warning("Invalid shares value: %s", data.get("shares"))
            data["shares"] = 0

        # Add tag if large trade
        data["is_large_trade"] = data["shares"] >= 10000

        return data
    except Exception as e:
        logger.exception("❌ Error processing insider data: %s", e)
        data["processing_error"] = str(e)
        return data
