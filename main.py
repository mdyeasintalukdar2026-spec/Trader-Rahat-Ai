import asyncio
import logging
import os
from pyquotex.stable_api import Quotex
from app import start_server, RENDER_SERVER_URL
from strategy import UltraProMaxStrategy, KNOWLEDGE_REGISTRY, API_REGISTRY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("UltraProMaxMasterRunner")


def detect_active_market(client: Quotex) -> str:
    env_asset = os.environ.get("QX_ASSET", "").strip()
    if env_asset:
        return env_asset
    for attr in ("current_asset", "active_asset", "selected_asset"):
        val = getattr(client, attr, None)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return "EURUSD_otc"


async def main():
    start_server()
    logger.info(f"Flask Keep-Alive Server Started Successfully on {RENDER_SERVER_URL}")
    logger.info(
        f"Knowledge Matrix Ready: {KNOWLEDGE_REGISTRY['core_logic_rules_count']} Rules | "
        f"{KNOWLEDGE_REGISTRY['pro_max_modules_count']} Pro-Max Modules | "
        f"{KNOWLEDGE_REGISTRY['international_knowledge_nodes']:,} Nodes | "
        f"{len(API_REGISTRY)} API Endpoints"
    )

    client = Quotex(
        email=os.environ.get("QX_EMAIL", "your_quotex_email@gmail.com"),
        password=os.environ.get("QX_PASSWORD", "your_quotex_password"),
        lang="en",
        host="qxbroker.com"
    )

    logger.info("Connecting to Quotex WebSocket Live Server...")
    check, reason = await client.connect()

    if check:
        logger.info("SUCCESS: Connected to Quotex Direct Live Data Stream!")

        active_asset = detect_active_market(client)
        stake_amount = float(os.environ.get("QX_STAKE", "1.0"))
        duration = int(os.environ.get("QX_DURATION", "60"))

        await client.subscribe_candles(active_asset, duration)
        logger.info(f"ULTRA-PRO MAX QUANTITATIVE ENGINE ACTIVE: Scanning {active_asset}...")

        while True:
            try:
                detected_asset = detect_active_market(client)
                if detected_asset != active_asset:
                    active_asset = detected_asset
                    await client.subscribe_candles(active_asset, duration)
                    logger.info(f"Market Auto-Detected & Switched: {active_asset}")

                _, formatted_sym, is_otc = UltraProMaxStrategy.normalize_symbol(active_asset)
                base_curr = formatted_sym.split("/")[0] if "/" in formatted_sym else "USD"

                if not is_otc and not UltraProMaxStrategy.check_news_safety(base_curr):
                    await asyncio.sleep(60)
                    continue

                if not UltraProMaxStrategy.check_payout_safety(active_asset, 80.0):
                    await asyncio.sleep(15)
                    continue

                live_candles = client.get_realtime_candles(active_asset)

                if live_candles and len(live_candles) >= 20:
                    tech_analysis = UltraProMaxStrategy.calculate_indicators(live_candles, asset=active_asset)
                    tech_signal = tech_analysis.get("signal")

                    logger.info(
                        f"Metrics [{active_asset}]: RSI={tech_analysis.get('rsi')} | "
                        f"MACD_H={tech_analysis.get('macd_hist')} | Signal={tech_signal} | "
                        f"Confidence={tech_analysis.get('confidence')}%"
                    )

                    if tech_signal in ["CALL", "PUT"]:
                        market_summary = (
                            f"Asset: {active_asset}, Technical Signal: {tech_signal}, "
                            f"Indicators: {tech_analysis}, Recent Candles Close: {[c.get('close') for c in live_candles[-5:]]}"
                        )
                        ai_decision = UltraProMaxStrategy.verify_via_groq_ai(market_summary, fallback_signal=tech_signal)
                        logger.info(f"Groq AI Arbiter Consensus: {ai_decision} (Technical: {tech_signal})")

                        if ai_decision == tech_signal and ai_decision in ["CALL", "PUT"]:
                            logger.info(
                                f"[VERIFIED MULTI-CONFLUENCE SIGNAL] {ai_decision} on {active_asset} | "
                                f"Stake: ${stake_amount} | Expiry: {duration}s"
                            )
                else:
                    logger.info("Accumulating sufficient real-time candle feed...")

                await asyncio.sleep(1.5)

            except Exception as e:
                logger.error(f"Error in Live Trading Loop: {e}")
                await asyncio.sleep(3)
    else:
        logger.error(f"Connection Failed: {reason}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually by user.")
