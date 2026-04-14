from __future__ import annotations

import argparse
import json
import logging
from numbers import Real

import spritter

_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch fuel prices")
    parser.add_argument("--provider", required=True, help="Provider name (e.g. JET, OMV, Avanti)")
    parser.add_argument("--id", required=True, help="Station identifier")
    parser.add_argument(
        "--user-agent",
        default=None,
        help="Override HTTP User-Agent header used for provider requests",
    )
    parser.add_argument("--json", action="store_true", help="Print raw JSON")
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=_LOG_LEVELS,
        help="Set logging verbosity",
    )
    return parser


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.WARNING),
        format="[%(levelname)s | %(name)s] %(message)s",
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    _configure_logging(args.log_level)

    logger = logging.getLogger(__name__)
    logger.info(
        "Fetching fuel prices via CLI provider=%s id=%s json=%s user_agent_set=%s",
        args.provider,
        args.id,
        args.json,
        bool(args.user_agent),
    )

    request = spritter.FuelStationRequest(
        provider=args.provider,
        station_id=args.id,
        user_agent=args.user_agent,
    )
    result = spritter.get_fuel_prices(request)
    prices = result.to_price_map()
    logger.info("Provider result received with %d entries", len(prices))
    logger.debug("Provider result payload: %s", prices)

    if args.json:
        print(json.dumps(prices, ensure_ascii=False))
        return

    for fuel_type, price in prices.items():
        if isinstance(price, Real):
            print(f"{fuel_type}: {float(price):.2f}")
            continue

        print(f"{fuel_type}: {price}")


if __name__ == "__main__":
    main()
