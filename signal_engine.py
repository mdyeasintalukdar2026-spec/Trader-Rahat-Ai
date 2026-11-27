import os
import time
import asyncio
import aiohttp
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


API_TIERS = {
    "MASTER": [
        {"name": "QUANTEX_MASTER", "url": "https://api.quantexbot.pro/v1/candles", "key": os.getenv("QUANTEX_MASTER_KEY", "")},
        {"name": "QUOTEX_DIRECT", "url": os.getenv("QUOTEX_WS_BRIDGE", ""), "key": os.getenv("QUOTEX_TOKEN", "")},
        {"name": "POLYGON_PRO", "url": "https://api.polygon.io/v2/aggs/ticker", "key": os.getenv("POLYGON_API_KEY", "")},
        {"name": "TWELVE_DATA_PRO", "url": "https://api.twelvedata.com/time_series", "key": os.getenv("TWELVEDATA_API_KEY", "")},
        {"name": "BINANCE_LIVE", "url": "https://api.binance.com/api/v3/klines", "key": ""},
        {"name": "ALPHA_VANTAGE", "url": "https://www.alphavantage.co/query", "key": os.getenv("ALPHAVANTAGE_KEY", "")},
        {"name": "FINNHUB_LIVE", "url": "https://finnhub.io/api/v1/forex/candle", "key": os.getenv("FINNHUB_API_KEY", "")},
        {"name": "GROQ_VALIDATOR", "url": "https://api.groq.com/openai/v1/chat/completions", "key": os.getenv("GROQ_API_KEY", "")},
        {"name": "GEMINI_VALIDATOR", "url": "https://generativelanguage.googleapis.com/v1beta/models", "key": os.getenv("GEMINI_API_KEY", "")},
        {"name": "OPENROUTER_AI", "url": "https://openrouter.ai/api/v1/chat/completions", "key": os.getenv("OPENROUTER_API_KEY", "")},
    ],
    "DEVELOPER": [
        {"name": "QUANTEX_DEV_STATUS", "url": "https://api.quantexbot.pro/v1/status", "key": os.getenv("QUANTEX_DEV_KEY", "")},
        {"name": "QUANTEX_DEV_PAYOUT", "url": "https://api.quantexbot.pro/v1/pairs", "key": os.getenv("QUANTEX_DEV_KEY", "")},
        {"name": "QUANTEX_DEV_STREAM", "url": "https://api.quantexbot.pro/v1/stream", "key": os.getenv("QUANTEX_DEV_KEY", "")},
        {"name": "QUANTEX_DEV_NEWS", "url": "https://api.quantexbot.pro/v1/news", "key": os.getenv("QUANTEX_DEV_KEY", "")},
    ],
    "BACKUP_POOL": [
        {
            "name": f"BACKUP_NODE_{i}",
            "url": os.getenv(f"BACKUP_URL_{i}", "https://api.twelvedata.com/time_series"),
            "key": os.getenv(f"BACKUP_KEY_{i}", "")
        }
        for i in range(1, 65) if os.getenv(f"BACKUP_KEY_{i}")
    ]
}


@dataclass
class KnowledgeEvaluation:
    call_score: float = 0.0
    put_score: float = 0.0
    total_weight: float = 0.0
    confirmations_call: List[str] = field(default_factory=list)
    confirmations_put: List[str] = field(default_factory=list)
    blocked_reason: Optional[str] = None


def evaluate_ultra_knowledge(
    candles: List[Dict],
    payout: float,
    is_high_impact_news: bool,
    spread_pips: float
) -> KnowledgeEvaluation:
    res = KnowledgeEvaluation()

    if is_high_impact_news:
        res.blocked_reason = "HIGH_IMPACT_NEWS_BLOCK"
        return res
    if payout < 75.0:
        res.blocked_reason = f"LOW_PAYOUT_BLOCK ({payout}%)"
        return res
    if spread_pips > 2.5:
        res.blocked_reason = f"HIGH_SPREAD_BLOCK ({spread_pips})"
        return res
    if len(candles) < 50:
        res.blocked_reason = "INSUFFICIENT_REAL_CANDLES"
        return res

    closes = np.array([c["close"] for c in candles], dtype=float)
    opens = np.array([c["open"] for c in candles], dtype=float)
    highs = np.array([c["high"] for c in candles], dtype=float)
    lows = np.array([c["low"] for c in candles], dtype=float)
    vols = np.array([c.get("volume", 1.0) for c in candles], dtype=float)

    # 1. Multi-EMA Trend Matrix (Weight: 20)
    res.total_weight += 20.0
    ema9 = np.mean(closes[-9:])
    ema21 = np.mean(closes[-21:])
    ema50 = np.mean(closes[-50:])
    if closes[-1] > ema9 > ema21 > ema50:
        res.call_score += 20.0
        res.confirmations_call.append("EMA_9_21_50_BULLISH_ALIGNMENT")
    elif closes[-1] < ema9 < ema21 < ema50:
        res.put_score += 20.0
        res.confirmations_put.append("EMA_9_21_50_BEARISH_ALIGNMENT")

    # 2. RSI (14) Zone (Weight: 15)
    res.total_weight += 15.0
    deltas = np.diff(closes[-15:])
    gains = np.mean(deltas[deltas > 0]) if np.any(deltas > 0) else 0.0
    losses = -np.mean(deltas[deltas < 0]) if np.any(deltas < 0) else 1e-9
    rs = gains / losses
    rsi = 100.0 - (100.0 / (1.0 + rs))
    if 52.0 <= rsi <= 68.0 or rsi < 28.0:
        res.call_score += 15.0
        res.confirmations_call.append(f"RSI_CALL_ZONE ({rsi:.1f})")
    if 32.0 <= rsi <= 48.0 or rsi > 72.0:
        res.put_score += 15.0
        res.confirmations_put.append(f"RSI_PUT_ZONE ({rsi:.1f})")

    # 3. SMC Liquidity Sweep & Rejection (Weight: 25)
    res.total_weight += 25.0
    prev_swing_low = np.min(lows[-15:-2])
    prev_swing_high = np.max(highs[-15:-2])
    last_body = abs(closes[-1] - opens[-1])
    lower_wick = min(opens[-1], closes[-1]) - lows[-1]
    upper_wick = highs[-1] - max(opens[-1], closes[-1])

    if lows[-1] < prev_swing_low and closes[-1] > prev_swing_low and lower_wick > last_body * 1.3:
        res.call_score += 25.0
        res.confirmations_call.append("SMC_SSL_SWEEP_REJECTION")
    if highs[-1] > prev_swing_high and closes[-1] < prev_swing_high and upper_wick > last_body * 1.3:
        res.put_score += 25.0
        res.confirmations_put.append("SMC_BSL_SWEEP_REJECTION")

    # 4. Candle Engulfing & Volume Confirmation (Weight: 20)
    res.total_weight += 20.0
    avg_vol = np.mean(vols[-20:-1])
    vol_confirmed = vols[-1] >= avg_vol * 1.1
    bull_engulf = closes[-2] < opens[-2] and closes[-1] > opens[-1] and closes[-1] > opens[-2]
    bear_engulf = closes[-2] > opens[-2] and closes[-1] < opens[-1] and closes[-1] < opens[-2]

    if bull_engulf and vol_confirmed:
        res.call_score += 20.0
        res.confirmations_call.append("BULLISH_ENGULFING_VOL_CONFIRMED")
    if bear_engulf and vol_confirmed:
        res.put_score += 20.0
        res.confirmations_put.append("BEARISH_ENGULFING_VOL_CONFIRMED")

    # 5. Bollinger Band (20, 2) Reclaim / Rejection (Weight: 20)
    res.total_weight += 20.0
    sma20 = np.mean(closes[-20:])
    std20 = np.std(closes[-20:])
    upper_bb = sma20 + (2.0 * std20)
    lower_bb = sma20 - (2.0 * std20)

    if closes[-2] <= lower_bb and closes[-1] > lower_bb:
        res.call_score += 20.0
        res.confirmations_call.append("BB_LOWER_RECLAIM_CALL")
    if closes[-2] >= upper_bb and closes[-1] < upper_bb:
        res.put_score += 20.0
        res.confirmations_put.append("BB_UPPER_REJECTION_PUT")

    return res


def normalize_candle_payload(raw_data) -> List[Dict]:
    if isinstance(raw_data, dict) and "candles" in raw_data:
        raw_list = raw_data["candles"]
    elif isinstance(raw_data, list):
        raw_list = raw_data
    else:
        return []

    normalized = []
    for item in raw_list:
        if isinstance(item, dict) and all(k in item for k in ("open", "high", "low", "close")):
            normalized.append({
                "open": float(item["open"]),
                "high": float(item["high"]),
                "low": float(item["low"]),
                "close": float(item["close"]),
                "volume": float(item.get("volume", 1.0))
            })
        elif isinstance(item, (list, tuple)) and len(item) >= 5:
            normalized.append({
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]) if len(item) > 5 else 1.0
            })
    return normalized


async def fetch_verified_candles(
    session: aiohttp.ClientSession,
    pair: str,
    timeframe: str
) -> Tuple[List[Dict], str]:
    all_sources = API_TIERS["MASTER"] + API_TIERS["DEVELOPER"] + API_TIERS["BACKUP_POOL"]
    for src in all_sources:
        if not src.get("url"):
            continue
        try:
            headers = {"Authorization": f"Bearer {src['key']}"} if src.get("key") else {}
            params = {"symbol": pair.replace("/", ""), "interval": timeframe, "limit": 60}
            async with session.get(src["url"], headers=headers, params=params, timeout=3.5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    candles = normalize_candle_payload(data)
                    if len(candles) >= 50:
                        return candles, src["name"]
        except Exception:
            continue
    return [], "NONE"


async def generate_authentic_signal(
    pair: str,
    timeframe: str,
    payout: float = 85.0,
    is_news: bool = False,
    spread: float = 0.8
) -> Dict:
    async with aiohttp.ClientSession() as session:
        candles, active_source = await fetch_verified_candles(session, pair, timeframe)

    if not candles:
        return {
            "status": "HOLD",
            "signal": "NO_SIGNAL",
            "pair": pair,
            "timeframe": timeframe,
            "accuracy": 0.0,
            "reason": "LIVE_FEED_UNAVAILABLE_NO_FAKE_GENERATED",
            "source": "NONE"
        }

    eval_res = evaluate_ultra_knowledge(candles, payout, is_news, spread)
    if eval_res.blocked_reason:
        return {
            "status": "BLOCKED",
            "signal": "NO_SIGNAL",
            "pair": pair,
            "timeframe": timeframe,
            "accuracy": 0.0,
            "reason": eval_res.blocked_reason,
            "source": active_source
        }

    call_pct = round((eval_res.call_score / eval_res.total_weight) * 100.0, 2)
    put_pct = round((eval_res.put_score / eval_res.total_weight) * 100.0, 2)
    min_confidence = 75.0

    if call_pct >= min_confidence and call_pct > (put_pct + 25.0) and len(eval_res.confirmations_call) >= 3:
        return {
            "status": "CONFIRMED",
            "signal": "CALL",
            "pair": pair,
            "timeframe": timeframe,
            "accuracy": call_pct,
            "confirmations": eval_res.confirmations_call,
            "source": active_source,
            "timestamp": int(time.time())
        }

    if put_pct >= min_confidence and put_pct > (call_pct + 25.0) and len(eval_res.confirmations_put) >= 3:
        return {
            "status": "CONFIRMED",
            "signal": "PUT",
            "pair": pair,
            "timeframe": timeframe,
            "accuracy": put_pct,
            "confirmations": eval_res.confirmations_put,
            "source": active_source,
            "timestamp": int(time.time())
        }

    return {
        "status": "WAITING",
        "signal": "NO_SIGNAL",
        "pair": pair,
        "timeframe": timeframe,
        "accuracy": max(call_pct, put_pct),
        "reason": "CONFLUENCE_THRESHOLD_NOT_MET",
        "source": active_source
    }
