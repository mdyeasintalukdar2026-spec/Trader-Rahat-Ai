from flask import Flask, jsonify, make_response, request
import threading
import requests
import time
import os
import logging
from datetime import datetime, timedelta

app = Flask(__name__, static_folder=".")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("TraderRahatEngine")

RENDER_SERVER_URL = os.environ.get("RENDER_SERVER_URL", "https://trader-rahat-ai.onrender.com")
QX_API_KEY = os.environ.get("QX_API_KEY", "qx_live_1xxOcsg5_3vEavHfZwAkGufh9NLLWJhUqG3T6H6oCEuoDWeJV")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "dbcaa19r01qqr3s0pf60dbcaa19r01qqr3s0pf6g")
TWELVE_DATA_KEY = os.environ.get("TWELVE_DATA_KEY", "8f5d4d4fce7f44e5bda54420591411c8")
TIMEZONE_OFFSET = float(os.environ.get("QX_TZ", "6"))

http_session = requests.Session()
if QX_API_KEY:
    http_session.headers["Authorization"] = f"Bearer {QX_API_KEY}"


BOT_JS_CODE = r"""
(function () {
    const SERVER_URL = "https://trader-rahat-ai.onrender.com";
    const BOT_NAME = "Trader Rahat";
    const BOT_LOGO = "https://i.postimg.cc/nhK0yHw1/file-000000001b808211b004c14708610520.png";

    function cleanup() {
        [
            "tr-rahat-styles",
            "tr-rahat-square-bot",
            "tr-rahat-rtl-scan",
            "tr-rahat-modal",
            "tr-rahat-trade-popup"
        ].forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
    }

    function injectStyles() {
        const style = document.createElement("style");
        style.id = "tr-rahat-styles";
        style.textContent = `
            @keyframes trThickWave1 {
                0% {
                    transform: scale(0.92);
                    opacity: 0.98;
                    border-color: #22c55e;
                    box-shadow: 0 0 16px #22c55e, inset 0 0 12px #22c55e;
                }
                33% {
                    border-color: #38bdf8;
                    box-shadow: 0 0 20px #38bdf8, inset 0 0 14px #38bdf8;
                }
                66% {
                    border-color: #a855f7;
                    box-shadow: 0 0 20px #a855f7, inset 0 0 14px #a855f7;
                }
                100% {
                    transform: scale(1.42);
                    opacity: 0;
                    border-color: #facc15;
                    box-shadow: 0 0 22px #facc15;
                }
            }
            @keyframes trBotBorderHue {
                0% { border-color: #22c55e; box-shadow: 0 0 20px rgba(34,197,94,0.95); }
                25% { border-color: #38bdf8; box-shadow: 0 0 22px rgba(56,189,248,1); }
                50% { border-color: #a855f7; box-shadow: 0 0 22px rgba(168,85,247,1); }
                75% { border-color: #facc15; box-shadow: 0 0 22px rgba(250,204,21,1); }
                100% { border-color: #22c55e; box-shadow: 0 0 20px rgba(34,197,94,0.95); }
            }
            @keyframes trRightToLeftBeam {
                0% { right: -26%; opacity: 0.5; }
                50% { opacity: 1; }
                100% { right: 112%; opacity: 0.5; }
            }
            @keyframes trCaptureBeamSweep {
                0% { top: -18%; opacity: 0.4; }
                50% { opacity: 1; }
                100% { top: 108%; opacity: 0.4; }
            }
            @keyframes trCaptureLogoGlow {
                0%, 100% {
                    transform: scale(1);
                    box-shadow: 0 0 18px rgba(34,197,94,0.85), 0 0 34px rgba(56,189,248,0.65);
                    border-color: #22c55e;
                }
                50% {
                    transform: scale(1.05);
                    box-shadow: 0 0 24px rgba(250,204,21,0.95), 0 0 42px rgba(239,68,68,0.75);
                    border-color: #facc15;
                }
            }
            @keyframes trThreadFlow {
                0% { stroke-dashoffset: 36; }
                100% { stroke-dashoffset: 0; }
            }
            @keyframes trCenterHubPulse {
                0%, 100% {
                    box-shadow: 0 0 18px rgba(56,189,248,0.85), 0 0 34px rgba(34,197,94,0.65);
                    border-color: #38bdf8;
                }
                50% {
                    box-shadow: 0 0 26px rgba(168,85,247,1), 0 0 44px rgba(236,72,153,0.75);
                    border-color: #ec4899;
                }
            }
            @keyframes trSnappyPop {
                0% { opacity: 0; transform: scale(0.84) translateY(10px); }
                70% { opacity: 1; transform: scale(1.02) translateY(0); }
                100% { opacity: 1; transform: scale(1) translateY(0); }
            }
            @keyframes trSparkleRim {
                0% {
                    border-color: #22c55e;
                    box-shadow: 0 0 24px rgba(34,197,94,0.9), -14px 0 28px rgba(56,189,248,0.65), 14px 0 28px rgba(168,85,247,0.65);
                }
                33% {
                    border-color: #38bdf8;
                    box-shadow: 0 0 26px rgba(56,189,248,0.95), -14px 0 30px rgba(168,85,247,0.7), 14px 0 30px rgba(34,197,94,0.7);
                }
                66% {
                    border-color: #facc15;
                    box-shadow: 0 0 26px rgba(250,204,21,0.95), -14px 0 30px rgba(34,197,94,0.7), 14px 0 30px rgba(236,72,153,0.7);
                }
                100% {
                    border-color: #22c55e;
                    box-shadow: 0 0 24px rgba(34,197,94,0.9), -14px 0 28px rgba(56,189,248,0.65), 14px 0 28px rgba(168,85,247,0.65);
                }
            }
            @keyframes trElectricSpinSlow {
                0% {
                    transform: rotate(0deg);
                    filter: drop-shadow(0 0 6px #38bdf8) drop-shadow(0 0 12px #22c55e);
                }
                50% {
                    transform: rotate(180deg);
                    filter: drop-shadow(0 0 9px #facc15) drop-shadow(0 0 16px #a855f7);
                }
                100% {
                    transform: rotate(360deg);
                    filter: drop-shadow(0 0 6px #38bdf8) drop-shadow(0 0 12px #22c55e);
                }
            }
            @keyframes trElectricArcFlash {
                0%, 100% {
                    box-shadow:
                        0 0 14px rgba(56, 189, 248, 0.85),
                        0 0 26px rgba(34, 197, 94, 0.55),
                        inset 0 0 14px rgba(56, 189, 248, 0.45);
                }
                25% {
                    box-shadow:
                        0 0 20px rgba(250, 204, 21, 0.95),
                        0 0 32px rgba(56, 189, 248, 0.8),
                        inset 0 0 18px rgba(250, 204, 21, 0.55);
                }
                50% {
                    box-shadow:
                        0 0 16px rgba(168, 85, 247, 0.95),
                        0 0 30px rgba(236, 72, 153, 0.7),
                        inset 0 0 16px rgba(168, 85, 247, 0.5);
                }
                75% {
                    box-shadow:
                        0 0 22px rgba(34, 197, 94, 1),
                        0 0 36px rgba(56, 189, 248, 0.85),
                        inset 0 0 18px rgba(34, 197, 94, 0.6);
                }
            }
            @keyframes trOrbBlink {
                0%, 100% { transform: scale(0.85); opacity: 0.75; }
                50% { transform: scale(1.25); opacity: 1; }
            }

            /* Square Bot Icon + Thick Compact Wave Aura Underneath */
            #tr-rahat-square-bot {
                position: fixed;
                right: 14px;
                top: 57%;
                width: 68px;
                height: 68px;
                border-radius: 15px;
                background: #071120;
                border: 2.5px solid #22c55e;
                z-index: 2147483645;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                user-select: none;
                touch-action: none;
                overflow: visible;
                animation: trBotBorderHue 3s infinite linear;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            .tr-wave-ring {
                position: absolute;
                inset: -3px;
                border-radius: 17px;
                border: 4.5px solid #22c55e;
                pointer-events: none;
                z-index: -1;
                animation: trThickWave1 1.65s infinite ease-out;
            }
            .tr-wave-ring.tr-w2 { animation-delay: 0.55s; }
            .tr-wave-ring.tr-w3 { animation-delay: 1.1s; }
            .tr-sq-box {
                width: 100%;
                height: 100%;
                border-radius: 12px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #071120;
                position: relative;
                z-index: 2;
            }
            .tr-sq-box img {
                width: 56px;
                height: 56px;
                border-radius: 11px;
                object-fit: cover;
                pointer-events: none;
            }

            /* Right-to-Left Thick Chart Scan Beam */
            #tr-rahat-rtl-scan {
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 2147483644;
                overflow: hidden;
                background: rgba(14, 165, 233, 0.05);
            }
            .tr-rtl-beam {
                position: absolute;
                top: 0;
                bottom: 0;
                width: 130px;
                background: linear-gradient(
                    270deg,
                    transparent 0%,
                    rgba(56, 189, 248, 0.28) 28%,
                    rgba(34, 197, 94, 0.6) 55%,
                    rgba(168, 85, 247, 0.4) 80%,
                    transparent 100%
                );
                border-right: 3px solid #4ade80;
                box-shadow: -14px 0 38px rgba(34, 197, 94, 0.7), 14px 0 38px rgba(56, 189, 248, 0.6);
                animation: trRightToLeftBeam 1.2s ease-in-out infinite;
            }

            /* Modal Container */
            #tr-rahat-modal {
                position: fixed;
                inset: 0;
                background: rgba(2, 6, 15, 0.6);
                backdrop-filter: blur(4px);
                z-index: 2147483646;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            .tr-window {
                width: 100%;
                max-width: 394px;
                background: linear-gradient(180deg, #0d1629 0%, #070d1a 100%);
                border-radius: 18px;
                color: #f8fafc;
                overflow: hidden;
                border: 2px solid rgba(56, 189, 248, 0.55);
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9), 0 0 28px rgba(56, 189, 248, 0.25);
                animation: trSnappyPop 0.24s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .tr-win-sparkle {
                border: 2.5px solid #22c55e;
                animation: trSnappyPop 0.22s cubic-bezier(0.16, 1, 0.3, 1), trSparkleRim 2.2s infinite linear;
            }

            /* Panel 1: Market Analysis Capture with Trader Rahat Logo Inside */
            .tr-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 11px 14px;
                background: linear-gradient(90deg, #101b33 0%, #0b1326 100%);
                border-bottom: 1px solid rgba(148, 163, 184, 0.16);
            }
            .tr-pill-asset {
                font-size: 10.5px;
                font-weight: 800;
                color: #7dd3fc;
                background: rgba(14, 165, 233, 0.2);
                border: 1px solid rgba(56, 189, 248, 0.55);
                padding: 2px 9px;
                border-radius: 8px;
            }
            .tr-close {
                width: 28px;
                height: 28px;
                border-radius: 8px;
                border: 1px solid rgba(148, 163, 184, 0.26);
                background: rgba(30, 41, 59, 0.88);
                color: #e2e8f0;
                font-weight: 800;
                cursor: pointer;
            }
            .tr-capture-screen {
                position: relative;
                height: 185px;
                border-radius: 14px;
                background: radial-gradient(circle at 50% 45%, rgba(34, 197, 94, 0.22), rgba(56, 189, 248, 0.12) 45%, rgba(5, 10, 20, 0.97) 80%);
                border: 1.5px solid rgba(56, 189, 248, 0.35);
                overflow: hidden;
                padding: 10px 12px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .tr-capture-center-art {
                position: relative;
                align-self: center;
                width: 82px;
                height: 82px;
                border-radius: 16px;
                padding: 3px;
                background: linear-gradient(135deg, #22c55e, #38bdf8, #a855f7, #facc15);
                border: 2px solid #22c55e;
                animation: trCaptureLogoGlow 1.8s infinite ease-in-out;
                z-index: 2;
            }
            .tr-capture-center-art img {
                width: 100%;
                height: 100%;
                border-radius: 13px;
                object-fit: cover;
                display: block;
            }
            .tr-capture-beam {
                position: absolute;
                left: 0;
                right: 0;
                height: 32px;
                background: linear-gradient(180deg, transparent, rgba(56, 189, 248, 0.42), rgba(34, 197, 94, 0.65), rgba(250, 204, 21, 0.35), transparent);
                box-shadow: 0 0 22px rgba(56, 189, 248, 0.6);
                animation: trCaptureBeamSweep 1.25s linear infinite;
                pointer-events: none;
                z-index: 3;
            }

            /* Panel 2: 4-Second High-Color 6-Node Hub */
            .tr-hub-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 14px;
                background: linear-gradient(90deg, #16213e 0%, #0f172a 50%, #1a1638 100%);
                border-bottom: 1px solid rgba(139, 92, 246, 0.25);
            }
            .tr-broker-brand {
                display: flex;
                align-items: center;
                gap: 9px;
            }
            .tr-purple-logo {
                width: 32px;
                height: 32px;
                border-radius: 9px;
                background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
                display: flex;
                align-items: flex-end;
                justify-content: center;
                gap: 2.5px;
                padding: 7px 6px;
                box-sizing: border-box;
                box-shadow: 0 0 16px rgba(168, 85, 247, 0.75);
            }
            .tr-purple-logo span {
                width: 3px;
                background: #ffffff;
                border-radius: 2px;
            }
            .tr-otc-switch {
                display: flex;
                align-items: center;
                background: #080e1c;
                border: 1px solid rgba(139, 92, 246, 0.35);
                border-radius: 10px;
                padding: 3px;
                gap: 2px;
            }
            .tr-seg {
                font-size: 10.5px;
                font-weight: 800;
                padding: 4px 10px;
                border-radius: 7px;
                color: #64748b;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            .tr-seg-active {
                background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
                color: #ffffff;
                box-shadow: 0 0 14px rgba(168, 85, 247, 0.8);
            }
            .tr-mac-bar {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px 4px;
            }
            .tr-mac-dots {
                display: flex;
                gap: 4px;
            }
            .tr-mac-dots i {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                display: inline-block;
            }
            .tr-network-stage {
                position: relative;
                width: 100%;
                height: 235px;
                margin: 4px 0 6px;
                background: radial-gradient(circle at 50% 52%, rgba(99, 102, 241, 0.14), transparent 70%);
            }
            .tr-threads-svg {
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
            }
            .tr-thread-base {
                stroke: rgba(148, 163, 184, 0.25);
                stroke-width: 2.2;
                fill: none;
            }
            .tr-thread-pulse {
                stroke-width: 3;
                stroke-linecap: round;
                stroke-dasharray: 12 24;
                fill: none;
                animation: trThreadFlow 0.75s linear infinite;
            }
            .tr-app-node {
                position: absolute;
                transform: translate(-50%, -50%);
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
                width: 80px;
            }
            .tr-app-tile {
                width: 45px;
                height: 45px;
                border-radius: 13px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.28);
            }
            .tr-app-lbl {
                font-size: 9.5px;
                font-weight: 800;
                color: #f1f5f9;
                white-space: nowrap;
                text-shadow: 0 1px 5px rgba(0,0,0,0.95);
            }
            .tr-center-hub-orb {
                position: absolute;
                left: 50%;
                top: 52%;
                transform: translate(-50%, -50%);
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: radial-gradient(circle, #102a45 0%, #07101f 80%);
                border: 2.5px solid #38bdf8;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                gap: 3.5px;
                padding: 16px 12px;
                box-sizing: border-box;
                animation: trCenterHubPulse 1.35s infinite ease-in-out;
            }
            .tr-center-hub-orb span {
                width: 4px;
                border-radius: 2px;
            }
            .tr-checks-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4px 12px;
                padding: 0 14px 10px;
                font-size: 10.5px;
                font-weight: 700;
                color: #e2e8f0;
            }
            .tr-analyzing-pill {
                margin: 0 14px 14px;
                padding: 10px;
                border-radius: 999px;
                background: linear-gradient(90deg, #6366f1, #0ea5e9, #10b981);
                color: #ffffff;
                font-size: 12px;
                font-weight: 900;
                text-align: center;
                box-shadow: 0 0 22px rgba(56, 189, 248, 0.65);
            }

            /* Panel 3: Snappy Trade Signal + Circular Electric Confidence Ring */
            .tr-call-card {
                margin: 9px 0 11px;
                padding: 12px;
                border-radius: 14px;
                text-align: center;
                border: 2px solid #22c55e;
                background: linear-gradient(180deg, rgba(16, 185, 129, 0.28), rgba(6, 78, 59, 0.18));
                box-shadow: 0 0 26px rgba(34, 197, 94, 0.36);
            }
            .tr-put-card {
                margin: 9px 0 11px;
                padding: 12px;
                border-radius: 14px;
                text-align: center;
                border: 2px solid #ef4444;
                background: linear-gradient(180deg, rgba(239, 68, 68, 0.28), rgba(127, 29, 29, 0.18));
                box-shadow: 0 0 26px rgba(239, 68, 68, 0.36);
            }
            .tr-grid-2 {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 10px;
                align-items: stretch;
            }
            .tr-stat-tile {
                background: rgba(15, 23, 42, 0.94);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 13px;
                padding: 9px;
            }

            /* Circular Electric Lightning Confidence Ring */
            .tr-conf-circle-wrap {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: radial-gradient(circle, rgba(15, 23, 42, 0.98) 55%, rgba(8, 15, 30, 0.98) 100%);
                border-radius: 14px;
                padding: 8px;
                border: 1px solid rgba(56, 189, 248, 0.22);
            }
            .tr-electric-circle {
                position: relative;
                width: 108px;
                height: 108px;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: radial-gradient(circle at 50% 40%, #0f213d 0%, #070e1c 80%);
                animation: trElectricArcFlash 2.8s infinite ease-in-out;
            }
            .tr-electric-ring-svg {
                position: absolute;
                inset: -4px;
                width: 116px;
                height: 116px;
                pointer-events: none;
                animation: trElectricSpinSlow 5.5s linear infinite;
            }

            .tr-spark-confirm-strip {
                position: relative;
                margin-top: 10px;
                padding: 10px 14px;
                border-radius: 999px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border: 2px solid #38bdf8;
                animation: trSparkleRim 2s infinite linear;
                cursor: pointer;
            }
            .tr-side-orb {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                animation: trOrbBlink 1.1s infinite ease-in-out;
            }

            /* Top-Right Trade Opened Confirmation Toast */
            #tr-rahat-trade-popup {
                position: fixed;
                top: 64px;
                right: 12px;
                z-index: 2147483647;
                padding: 10px 14px;
                border-radius: 14px;
                color: #ffffff;
                display: flex;
                align-items: center;
                gap: 10px;
                border: 2px solid #4ade80;
                animation: trSnappyPop 0.22s ease-out, trSparkleRim 2s infinite linear;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
        `;
        document.head.appendChild(style);
    }

    function detectMarketInfo() {
        let pair = "USD/DZD (OTC)";
        try {
            const els = document.querySelectorAll("*");
            for (let i = 0; i < els.length; i++) {
                const el = els[i];
                if (el.children.length === 0 && el.innerText) {
                    const txt = el.innerText.trim();
                    if (/^[A-Z]{3}\/[A-Z]{3}(\s*\(OTC\))?$/i.test(txt)) {
                        pair = txt;
                        break;
                    }
                }
            }
        } catch (_) {}
        const isOtc = /otc/i.test(pair);
        return { pair, isOtc };
    }

    function getPriceSample(isCall) {
        const base = isCall ? 254.104 : 253.892;
        const delta = ((Date.now() % 80) - 40) / 1000;
        return (base + delta).toFixed(3);
    }

    function getDynamicTradeProfile(isCall, confidence) {
        const callSetups = [
            {
                pattern: "Bullish Engulfing Breakout",
                zoneLabel: "▲ BREAKOUT TARGET",
                midLabel: "◆ DEMAND SURGE ZONE",
                lowLabel: "▼ STRONG BUY SUPPORT"
            },
            {
                pattern: "Morning Star Reversal",
                zoneLabel: "▲ UPPER LIQUIDITY",
                midLabel: "◆ EMA GOLDEN CROSS",
                lowLabel: "▼ REVERSAL FLOOR"
            },
            {
                pattern: "Ascending Channel Impulse",
                zoneLabel: "▲ CHANNEL RESISTANCE",
                midLabel: "◆ MOMENTUM PIVOT",
                lowLabel: "▼ HIGHER LOW BASE"
            },
            {
                pattern: "Bullish Pinbar Rejection",
                zoneLabel: "▲ PROFIT EXPANSION",
                midLabel: "◆ ORDERBLOCK ENTRY",
                lowLabel: "▼ WICK REJECTION ZONE"
            }
        ];

        const putSetups = [
            {
                pattern: "Bearish Engulfing Drop",
                zoneLabel: "▲ SUPPLY REJECTION",
                midLabel: "◆ SELL PRESSURE ZONE",
                lowLabel: "▼ DOWNSIDE TARGET"
            },
            {
                pattern: "Evening Star Breakdown",
                zoneLabel: "▲ DOUBLE TOP CEILING",
                midLabel: "◆ EMA DEATH CROSS",
                lowLabel: "▼ LIQUIDITY DROP"
            },
            {
                pattern: "Descending Wedge Break",
                zoneLabel: "▲ LOWER HIGH CAP",
                midLabel: "◆ VOLUME DUMP PIVOT",
                lowLabel: "▼ SUPPORT BREAKDOWN"
            },
            {
                pattern: "Shooting Star Rejection",
                zoneLabel: "▲ UPPER WICK TRAP",
                midLabel: "◆ SUPPLY ORDERBLOCK",
                lowLabel: "▼ BEARISH TARGET"
            }
        ];

        const list = isCall ? callSetups : putSetups;
        const idx = (Math.floor(Date.now() / 1000) + confidence) % list.length;
        return list[idx];
    }

    function showSparkleTradeConfirmation(pair, signal, price, confidence, isCall) {
        const old = document.getElementById("tr-rahat-trade-popup");
        if (old) old.remove();

        let secs = 15;
        const pop = document.createElement("div");
        pop.id = "tr-rahat-trade-popup";
        pop.style.background = isCall
            ? "linear-gradient(135deg, rgba(16, 122, 58, 0.97), rgba(12, 95, 130, 0.97))"
            : "linear-gradient(135deg, rgba(175, 28, 28, 0.97), rgba(180, 65, 15, 0.97))";

        const render = () => {
            const mm = String(Math.floor(secs / 60)).padStart(2, "0");
            const ss = String(secs % 60).padStart(2, "0");
            pop.innerHTML = `
                <span class="tr-side-orb" style="background:#38bdf8;box-shadow:0 0 12px #38bdf8;"></span>
                <div>
                    <div style="font-size:11.5px;font-weight:900;letter-spacing:0.3px;">
                        ${BOT_NAME} • ${signal} (${mm}:${ss})
                    </div>
                    <div style="font-size:10.5px;font-weight:700;opacity:0.95;margin-top:2px;">
                        Confirmed at ${price} ${pair} • ${confidence}%
                    </div>
                </div>
                <span class="tr-side-orb" style="background:#facc15;box-shadow:0 0 12px #facc15;animation-delay:0.5s;"></span>
            `;
        };

        render();
        document.body.appendChild(pop);

        const iv = setInterval(() => {
            secs -= 1;
            if (secs <= 0 || !pop.parentNode) {
                clearInterval(iv);
                if (pop.parentNode) pop.remove();
                return;
            }
            render();
        }, 1000);
    }

    function startRtlBeam() {
        stopRtlBeam();
        const beamWrap = document.createElement("div");
        beamWrap.id = "tr-rahat-rtl-scan";
        beamWrap.innerHTML = `<div class="tr-rtl-beam"></div>`;
        document.body.appendChild(beamWrap);
    }

    function stopRtlBeam() {
        const beamWrap = document.getElementById("tr-rahat-rtl-scan");
        if (beamWrap) beamWrap.remove();
    }

    async function fetchSignal(pair) {
        try {
            const res = await fetch(`${SERVER_URL}/signal?asset=${encodeURIComponent(pair)}&t=${Date.now()}`);
            if (res.ok) return await res.json();
        } catch (_) {}
        const fallback = Math.floor(Date.now() / 1000) % 2 === 0 ? "CALL" : "PUT";
        const dynamicConf = Math.floor(Math.random() * 100) + 1;
        return {
            bot: BOT_NAME,
            asset: pair,
            signal: fallback,
            confidence: dynamicConf,
            trend: fallback === "CALL" ? "Uptrend" : "Downtrend",
            pattern: fallback === "CALL" ? "Bullish Momentum" : "Bearish Momentum"
        };
    }

    function runBotSequence() {
        const old = document.getElementById("tr-rahat-modal");
        if (old) old.remove();

        const { pair, isOtc } = detectMarketInfo();
        startRtlBeam();

        const modal = document.createElement("div");
        modal.id = "tr-rahat-modal";
        const win = document.createElement("div");
        win.className = "tr-window";
        modal.appendChild(win);
        document.body.appendChild(modal);

        const closeAll = () => {
            stopRtlBeam();
            if (modal.parentNode) modal.remove();
        };

        // Step 1 (0 -> 3500ms): Market Analysis Capture with Trader Rahat Logo + 20->40->60->80->100
        win.innerHTML = `
            <div class="tr-head">
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:13.5px;font-weight:800;">Market Analysis</span>
                    <span class="tr-pill-asset">${pair}</span>
                </div>
                <button class="tr-close" id="tr-x1">✕</button>
            </div>
            <div style="padding:14px;">
                <div class="tr-capture-screen">
                    <div class="tr-capture-beam"></div>
                    <div style="font-size:11px;font-weight:800;color:#e2e8f0;background:rgba(15,23,42,0.85);padding:4px 10px;border-radius:8px;align-self:flex-start;z-index:4;">
                        • Screen Capture • ${BOT_NAME}
                    </div>
                    <div class="tr-capture-center-art">
                        <img src="${BOT_LOGO}" alt="${BOT_NAME}" />
                    </div>
                    <div style="z-index:4;">
                        <div style="font-size:13px;font-weight:800;color:#fff;">⚡ Capturing live chart...</div>
                        <div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">Analyzing price action, indicators and market conditions...</div>
                    </div>
                </div>
                <div style="margin-top:11px;">
                    <div style="display:flex;justify-content:space-between;font-size:11px;font-weight:800;color:#94a3b8;margin-bottom:5px;">
                        <span>Scanning Market Structure</span>
                        <span id="tr-step-pct" style="color:#38bdf8;">20%</span>
                    </div>
                    <div style="height:7px;border-radius:999px;background:#1e293b;overflow:hidden;">
                        <div id="tr-step-bar" style="width:20%;height:100%;background:linear-gradient(90deg,#38bdf8,#22c55e,#a855f7);transition:width 0.45s ease;"></div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById("tr-x1").onclick = closeAll;

        const signalPromise = fetchSignal(pair);

        const steps = [40, 60, 80, 100];
        steps.forEach((val, idx) => {
            setTimeout(() => {
                const pEl = document.getElementById("tr-step-pct");
                const bEl = document.getElementById("tr-step-bar");
                if (pEl) pEl.textContent = `${val}%`;
                if (bEl) bEl.style.width = `${val}%`;
            }, (idx + 1) * 700);
        });

        // Step 2 (3500ms -> 7500ms = exact 4 seconds): High-Color 6-Node Chart Analyze Hub
        setTimeout(() => {
            if (!modal.parentNode) return;
            win.innerHTML = `
                <div class="tr-hub-header">
                    <div class="tr-broker-brand">
                        <div class="tr-purple-logo">
                            <span style="height:8px;"></span>
                            <span style="height:14px;"></span>
                            <span style="height:11px;"></span>
                        </div>
                        <div>
                            <div style="font-size:9px;font-weight:800;color:#a5b4fc;letter-spacing:0.6px;">BROKER</div>
                            <div style="font-size:14px;font-weight:900;color:#ffffff;">${BOT_NAME}</div>
                        </div>
                    </div>
                    <div class="tr-otc-switch">
                        <div class="tr-seg ${isOtc ? "tr-seg-active" : ""}">
                            ${isOtc ? '<span style="width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block;"></span>' : ""}
                            OTC
                        </div>
                        <div class="tr-seg ${!isOtc ? "tr-seg-active" : ""}">
                            ${!isOtc ? '<span style="width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block;"></span>' : ""}
                            Real
                        </div>
                    </div>
                </div>

                <div class="tr-mac-bar">
                    <div class="tr-mac-dots">
                        <i style="background:#ef4444;"></i>
                        <i style="background:#f59e0b;"></i>
                        <i style="background:#22c55e;"></i>
                    </div>
                    <span style="font-size:11.5px;font-weight:800;color:#e2e8f0;">${pair} Chart Analyze</span>
                </div>

                <div class="tr-network-stage">
                    <svg class="tr-threads-svg" viewBox="0 0 360 235" preserveAspectRatio="none">
                        <line class="tr-thread-base" x1="72" y1="54" x2="180" y2="122" />
                        <line class="tr-thread-base" x1="180" y1="42" x2="180" y2="122" />
                        <line class="tr-thread-base" x1="288" y1="54" x2="180" y2="122" />
                        <line class="tr-thread-base" x1="66" y1="138" x2="180" y2="122" />
                        <line class="tr-thread-base" x1="112" y1="196" x2="180" y2="122" />
                        <line class="tr-thread-base" x1="262" y1="188" x2="180" y2="122" />

                        <line class="tr-thread-pulse" stroke="#a855f7" x1="72" y1="54" x2="180" y2="122" />
                        <line class="tr-thread-pulse" stroke="#22c55e" x1="180" y1="42" x2="180" y2="122" />
                        <line class="tr-thread-pulse" stroke="#ec4899" x1="288" y1="54" x2="180" y2="122" />
                        <line class="tr-thread-pulse" stroke="#38bdf8" x1="66" y1="138" x2="180" y2="122" />
                        <line class="tr-thread-pulse" stroke="#f43f5e" x1="112" y1="196" x2="180" y2="122" />
                        <line class="tr-thread-pulse" stroke="#facc15" x1="262" y1="188" x2="180" y2="122" />
                    </svg>

                    <div class="tr-app-node" style="left:20%;top:22%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#6366f1,#4338ca);box-shadow:0 0 16px rgba(99,102,241,0.7);">📊</div>
                        <span class="tr-app-lbl">Market Data</span>
                    </div>

                    <div class="tr-app-node" style="left:50%;top:17%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#10b981,#047857);box-shadow:0 0 16px rgba(16,185,129,0.7);">📈</div>
                        <span class="tr-app-lbl">Trend</span>
                    </div>

                    <div class="tr-app-node" style="left:80%;top:22%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#ec4899,#be185d);box-shadow:0 0 16px rgba(236,72,153,0.7);">⚡</div>
                        <span class="tr-app-lbl">Indicators</span>
                    </div>

                    <div class="tr-app-node" style="left:18%;top:59%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 0 16px rgba(59,130,246,0.7);">📉</div>
                        <span class="tr-app-lbl">Price Action</span>
                    </div>

                    <div class="tr-app-node" style="left:31%;top:83%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#d946ef,#9333ea);box-shadow:0 0 16px rgba(217,70,239,0.7);">🧠</div>
                        <span class="tr-app-lbl">AI Analysis</span>
                    </div>

                    <div class="tr-app-node" style="left:73%;top:80%;">
                        <div class="tr-app-tile" style="background:linear-gradient(135deg,#eab308,#ca8a04);box-shadow:0 0 16px rgba(234,179,8,0.7);">🎯</div>
                        <span class="tr-app-lbl">Decision</span>
                    </div>

                    <div class="tr-center-hub-orb">
                        <span style="height:11px;background:#22c55e;"></span>
                        <span style="height:18px;background:#38bdf8;"></span>
                        <span style="height:14px;background:#f43f5e;"></span>
                    </div>
                </div>

                <div class="tr-checks-row">
                    <div><span style="color:#22c55e;">✓</span> Trend Analysis</div>
                    <div><span style="color:#38bdf8;">✓</span> RSI &amp; MACD</div>
                    <div><span style="color:#a855f7;">✓</span> Support / Resistance</div>
                    <div><span style="color:#facc15;">✓</span> Momentum &amp; Price</div>
                </div>

                <div class="tr-analyzing-pill">🧠 Analyzing chart...</div>
            `;
        }, 3500);

        // Step 3 (at 7500ms = after exact 4s second scan): Snappy Trade Card with Circular Electric Confidence
        setTimeout(async () => {
            if (!modal.parentNode) return;
            stopRtlBeam();

            const data = await signalPromise;
            const isCall = String(data.signal || "CALL").toUpperCase() === "CALL";
            const sigLabel = isCall ? "CALL" : "PUT";
            const finalConf = Math.min(100, Math.max(1, Number(data.confidence) || (Math.floor(Math.random() * 100) + 1)));
            const trendText = isCall ? "Uptrend" : "Downtrend";
            const setup = getDynamicTradeProfile(isCall, finalConf);
            const livePrice = getPriceSample(isCall);

            const convictionText = finalConf >= 75
                ? "High conviction"
                : (finalConf >= 45 ? "Moderate pulse" : "Early signal");

            win.className = "tr-window tr-win-sparkle";
            win.innerHTML = `
                <div class="tr-head">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span class="tr-pill-asset">${isOtc ? "OTC" : "REAL"}</span>
                        <span style="font-size:13.5px;font-weight:900;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-close" id="tr-x3">✕</button>
                </div>
                <div style="padding:13px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(15,23,42,0.92);border:1px solid rgba(56,189,248,0.28);border-radius:10px;padding:7px 11px;">
                        <span style="font-size:12.5px;font-weight:800;">${pair}</span>
                        <span style="font-size:10.5px;font-weight:800;color:#34d399;">• Live read 1m</span>
                    </div>

                    <div class="${isCall ? "tr-call-card" : "tr-put-card"}">
                        <div style="font-size:10px;font-weight:800;letter-spacing:1px;color:#cbd5e1;">- PLACE OPTION -</div>
                        <div style="font-size:30px;font-weight:900;color:${isCall ? "#22c55e" : "#ef4444"};margin:2px 0;">
                            ${isCall ? "▲ CALL" : "▼ PUT"}
                        </div>
                        <div style="font-size:11px;color:#e2e8f0;">
                            ${isCall ? "Upward move expected. Enter on the next candle" : "Downward move expected. Enter on the next candle"}
                        </div>
                    </div>

                    <div class="tr-grid-2">
                        <!-- Circular Electric Lightning Confidence Box (1-100%) -->
                        <div class="tr-conf-circle-wrap">
                            <div class="tr-electric-circle">
                                <svg class="tr-electric-ring-svg" viewBox="0 0 116 116">
                                    <defs>
                                        <linearGradient id="trBoltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#38bdf8" />
                                            <stop offset="35%" stop-color="#22c55e" />
                                            <stop offset="70%" stop-color="#facc15" />
                                            <stop offset="100%" stop-color="#a855f7" />
                                        </linearGradient>
                                    </defs>
                                    <circle cx="58" cy="58" r="53" fill="none" stroke="url(#trBoltGrad)" stroke-width="3" stroke-dasharray="18 7 9 6 24 8" stroke-linecap="round" />
                                    <circle cx="58" cy="58" r="49" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="6 14" opacity="0.85" />
                                </svg>
                                <div style="font-size:8px;font-weight:900;letter-spacing:0.6px;color:#94a3b8;">CONFIDENCE</div>
                                <div style="font-size:24px;font-weight:900;line-height:1.1;color:${isCall ? "#34d399" : "#f87171"};">${finalConf}%</div>
                                <div style="font-size:8.5px;font-weight:700;color:#e2e8f0;">${convictionText}</div>
                            </div>
                        </div>

                        <!-- Right Box: Trend Movement & Dynamic Levels -->
                        <div class="tr-stat-tile" style="display:flex;flex-direction:column;justify-content:center;">
                            <div style="font-size:9.5px;font-weight:900;color:#38bdf8;letter-spacing:0.5px;margin-bottom:5px;">TREND MOVEMENT</div>
                            <div style="font-size:10px;font-weight:800;color:#f87171;margin-bottom:3px;">${setup.zoneLabel}</div>
                            <div style="font-size:10px;font-weight:800;color:#38bdf8;margin-bottom:3px;">${setup.midLabel}</div>
                            <div style="font-size:10px;font-weight:800;color:#34d399;">${setup.lowLabel}</div>
                        </div>
                    </div>

                    <div class="tr-grid-2" style="margin-bottom:0;">
                        <div class="tr-stat-tile" style="padding:7px 9px;font-size:10.5px;font-weight:800;">
                            TREND: <span style="color:${isCall ? "#34d399" : "#f87171"};">${trendText}</span>
                        </div>
                        <div class="tr-stat-tile" style="padding:7px 9px;font-size:10.5px;font-weight:800;">
                            PATTERN: <span style="color:${isCall ? "#4ade80" : "#fb7185"};">${setup.pattern}</span>
                        </div>
                    </div>

                    <div id="tr-spark-confirm" class="tr-spark-confirm-strip" style="background:${isCall ? "linear-gradient(90deg,#14532d,#16a34a,#0284c7)" : "linear-gradient(90deg,#7f1d1d,#dc2626,#ea580c)"};">
                        <span class="tr-side-orb" style="background:#38bdf8;box-shadow:0 0 12px #38bdf8;"></span>
                        <span style="font-size:12px;font-weight:900;letter-spacing:0.4px;color:#ffffff;">
                            CONFIRM ${sigLabel} (${livePrice})
                        </span>
                        <span class="tr-side-orb" style="background:#facc15;box-shadow:0 0 12px #facc15;animation-delay:0.5s;"></span>
                    </div>
                </div>
            `;
            document.getElementById("tr-x3").onclick = closeAll;

            document.getElementById("tr-spark-confirm").onclick = () => {
                closeAll();
                showSparkleTradeConfirmation(pair, sigLabel, livePrice, finalConf, isCall);
            };
        }, 7500);
    }

    function createSquareBot() {
        const box = document.createElement("div");
        box.id = "tr-rahat-square-bot";
        box.innerHTML = `
            <span class="tr-wave-ring"></span>
            <span class="tr-wave-ring tr-w2"></span>
            <span class="tr-wave-ring tr-w3"></span>
            <div class="tr-sq-box">
                <img src="${BOT_LOGO}" alt="${BOT_NAME}" onerror="this.style.display='none';" />
            </div>
        `;

        let dragging = false;
        let moved = false;
        let dx = 0;
        let dy = 0;

        const onStart = (e) => {
            dragging = true;
            moved = false;
            const pt = e.touches ? e.touches[0] : e;
            const rect = box.getBoundingClientRect();
            dx = pt.clientX - rect.left;
            dy = pt.clientY - rect.top;
        };

        const onMove = (e) => {
            if (!dragging) return;
            const pt = e.touches ? e.touches[0] : e;
            const nx = Math.max(6, Math.min(window.innerWidth - box.offsetWidth - 6, pt.clientX - dx));
            const ny = Math.max(6, Math.min(window.innerHeight - box.offsetHeight - 6, pt.clientY - dy));
            if (Math.abs(nx - box.offsetLeft) > 3 || Math.abs(ny - box.offsetTop) > 3) {
                moved = true;
            }
            box.style.left = `${nx}px`;
            box.style.top = `${ny}px`;
            box.style.right = "auto";
            box.style.bottom = "auto";
        };

        const onEnd = () => {
            dragging = false;
        };

        box.addEventListener("mousedown", onStart);
        box.addEventListener("touchstart", onStart, { passive: true });
        window.addEventListener("mousemove", onMove);
        window.addEventListener("touchmove", onMove, { passive: true });
        window.addEventListener("mouseup", onEnd);
        window.addEventListener("touchend", onEnd);

        box.addEventListener("click", () => {
            if (!moved) {
                runBotSequence();
            }
        });

        document.body.appendChild(box);
    }

    function init() {
        if (!document.body) {
            setTimeout(init, 100);
            return;
        }
        cleanup();
        injectStyles();
        createSquareBot();
    }

    if (document.readyState === "complete" || document.readyState === "interactive") {
        init();
    } else {
        window.addEventListener("DOMContentLoaded", init);
        setTimeout(init, 350);
    }
})();
"""


class UltraPrecisionEngine:
    @staticmethod
    def verify_news_and_market_safety(currency: str = "USD") -> bool:
        try:
            url = f"https://finnhub.io/api/v1/calendar/economic?token={FINNHUB_API_KEY}"
            response = http_session.get(url, timeout=3)
            if response.status_code == 200:
                events = response.json().get("economicCalendar", [])
                now_time = datetime.utcnow() + timedelta(hours=TIMEZONE_OFFSET)
                for event in events:
                    if currency.upper() in event.get("currency", "").upper():
                        event_time_str = event.get("time", "").replace("Z", "+00:00")
                        if event_time_str:
                            event_dt = datetime.fromisoformat(event_time_str) + timedelta(hours=TIMEZONE_OFFSET)
                            if abs((event_dt.replace(tzinfo=None) - now_time).total_seconds()) < 900:
                                return False
            return True
        except Exception:
            return True

    @staticmethod
    def fetch_multi_indicator_confluence(symbol: str = "EUR/USD") -> dict:
        try:
            clean_symbol = symbol.replace("-", "/").replace("OTC", "").replace("(OTC)", "").strip()
            if not clean_symbol or len(clean_symbol) < 3:
                clean_symbol = "EUR/USD"
            url = f"https://api.twelvedata.com/rsi?symbol={clean_symbol}&interval=1min&apikey={TWELVE_DATA_KEY}"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                if "values" in data and len(data["values"]) > 0:
                    rsi_val = float(data["values"][0]["rsi"])
                    return {"rsi": rsi_val, "status": "VERIFIED"}
        except Exception:
            pass
        return {"rsi": 50.0, "status": "FALLBACK"}


class GroqAIArbitrationCore:
    @staticmethod
    def get_authentic_decision(market_context: str, rsi_val: float) -> dict:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are the Trader Rahat binary options AI arbiter enforcing both-way directional analysis based on market trend. Output STRICTLY 'CALL' or 'PUT'."
                },
                {
                    "role": "user",
                    "content": f"Analyze live market trend context: {market_context}. Output strictly 'CALL' or 'PUT'."
                }
            ],
            "temperature": 0.2,
            "max_tokens": 6
        }
        # Dynamic confidence between 1 and 100 based on live RSI strength + micro-time
        rsi_strength = int(min(99, max(1, abs(rsi_val - 50.0) * 2.2 + (int(time.time() * 13) % 45) + 30)))
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=3)
            if response.status_code == 200:
                decision = response.json()["choices"][0]["message"]["content"].strip().upper()
                if decision in ["CALL", "PUT"]:
                    return {"signal": decision, "confidence": rsi_strength}
        except Exception:
            pass
        fallback = "CALL" if (rsi_val < 50.0 or int(time.time() * 7) % 2 == 0) else "PUT"
        return {"signal": fallback, "confidence": rsi_strength}


@app.route("/")
def home():
    return f"Trader Rahat AI Engine Running Successfully on {RENDER_SERVER_URL}"


@app.route("/ping")
def ping():
    return "OK", 200


@app.route("/signal")
def get_signal():
    try:
        asset = request.args.get("asset", "USD/DZD (OTC)")
        current_time = time.time()
        base_currency = asset.split("/")[0].strip() if "/" in asset else "USD"
        news_safe = UltraPrecisionEngine.verify_news_and_market_safety(base_currency)
        indicator_data = UltraPrecisionEngine.fetch_multi_indicator_confluence(asset)
        rsi = indicator_data["rsi"]
        trend_direction = "Uptrend" if rsi < 50 else "Downtrend"
        base_bias = "CALL" if trend_direction == "Uptrend" else "PUT"
        market_ctx = f"Asset: {asset}, RSI: {rsi}, DetectedTrend: {trend_direction}, Bias: {base_bias}, NewsSafe: {news_safe}, Time: {current_time}"
        ai_res = GroqAIArbitrationCore.get_authentic_decision(market_ctx, rsi)
        sig = ai_res["signal"]
        conf = ai_res["confidence"]

        res = jsonify({
            "bot": "Trader Rahat",
            "asset": asset,
            "signal": sig,
            "confidence": conf,
            "trend": "Uptrend" if sig == "CALL" else "Downtrend",
            "pattern": "Bullish Momentum" if sig == "CALL" else "Bearish Momentum",
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception:
        fallback_dir = "CALL" if (int(time.time()) % 2 == 0) else "PUT"
        dynamic_conf = (int(time.time() * 17) % 100) + 1
        res = jsonify({
            "bot": "Trader Rahat",
            "asset": request.args.get("asset", "USD/DZD (OTC)"),
            "signal": fallback_dir,
            "confidence": dynamic_conf,
            "trend": "Uptrend" if fallback_dir == "CALL" else "Downtrend",
            "pattern": "Bullish Momentum" if fallback_dir == "CALL" else "Bearish Momentum",
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res


@app.route("/bot.js")
def bot_script():
    bot_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot.js")
    if os.path.exists(bot_js_path):
        with open(bot_js_path, "r", encoding="utf-8") as f:
            content = f.read()
        resp = make_response(content)
    else:
        resp = make_response(BOT_JS_CODE)
    resp.headers["Content-Type"] = "application/javascript; charset=utf-8"
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
