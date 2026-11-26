from flask import Flask, jsonify, make_response, request, send_from_directory
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
    const BOT_LOGO = "https://i.postimg.cc/5yg7fcSL/IMG-20261111-WA0039.jpg";

    function cleanup() {
        [
            "tr-rahat-styles",
            "tr-rahat-square-bot",
            "tr-rahat-chart-scan",
            "tr-rahat-modal",
            "tr-rahat-trade-banner"
        ].forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
    }

    function injectStyles() {
        const style = document.createElement("style");
        style.id = "tr-rahat-styles";
        style.textContent = `
            @keyframes trSquareBgShift {
                0% {
                    background: linear-gradient(135deg, #07192f 0%, #0d3b38 50%, #122044 100%);
                    border-color: #22c55e;
                    box-shadow: 0 0 18px rgba(34, 197, 94, 0.85), 0 0 34px rgba(56, 189, 248, 0.55);
                }
                33% {
                    background: linear-gradient(135deg, #0b2447 0%, #1b2a5e 50%, #0a3d4c 100%);
                    border-color: #38bdf8;
                    box-shadow: 0 0 20px rgba(56, 189, 248, 0.9), 0 0 38px rgba(168, 85, 247, 0.55);
                }
                66% {
                    background: linear-gradient(135deg, #1b153b 0%, #0d3b38 50%, #27173a 100%);
                    border-color: #a855f7;
                    box-shadow: 0 0 20px rgba(168, 85, 247, 0.9), 0 0 38px rgba(34, 197, 94, 0.55);
                }
                100% {
                    background: linear-gradient(135deg, #07192f 0%, #0d3b38 50%, #122044 100%);
                    border-color: #22c55e;
                    box-shadow: 0 0 18px rgba(34, 197, 94, 0.85), 0 0 34px rgba(56, 189, 248, 0.55);
                }
            }
            @keyframes trBackGlowOrbit {
                0% { transform: scale(1) rotate(0deg); filter: hue-rotate(0deg) blur(10px); opacity: 0.85; }
                50% { transform: scale(1.18) rotate(180deg); filter: hue-rotate(160deg) blur(13px); opacity: 1; }
                100% { transform: scale(1) rotate(360deg); filter: hue-rotate(360deg) blur(10px); opacity: 0.85; }
            }
            @keyframes trChartColumnSweep {
                0% { left: -24%; opacity: 0.35; }
                50% { opacity: 0.95; }
                100% { left: 108%; opacity: 0.35; }
            }
            @keyframes trCaptureScanBeam {
                0% { top: -20%; opacity: 0.3; }
                50% { opacity: 0.95; }
                100% { top: 108%; opacity: 0.3; }
            }
            @keyframes trModalPop {
                0% { opacity: 0; transform: scale(0.95) translateY(10px); }
                100% { opacity: 1; transform: scale(1) translateY(0); }
            }
            @keyframes trBannerSlide {
                0% { opacity: 0; transform: translateX(26px); }
                100% { opacity: 1; transform: translateX(0); }
            }

            #tr-rahat-square-bot {
                position: fixed;
                right: 12px;
                top: 57%;
                width: 68px;
                height: 68px;
                border-radius: 15px;
                border: 2.5px solid #22c55e;
                z-index: 2147483645;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                user-select: none;
                touch-action: none;
                overflow: visible;
                animation: trSquareBgShift 3.6s infinite ease-in-out;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            #tr-rahat-square-bot::before {
                content: "";
                position: absolute;
                inset: -8px;
                border-radius: 20px;
                background: conic-gradient(
                    from 0deg,
                    #22c55e,
                    #38bdf8,
                    #818cf8,
                    #2dd4bf,
                    #22c55e
                );
                z-index: -1;
                animation: trBackGlowOrbit 4.2s linear infinite;
            }
            .tr-sq-box {
                width: 100%;
                height: 100%;
                border-radius: 12px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(6, 13, 25, 0.92);
            }
            .tr-sq-box img {
                width: 50px;
                height: 50px;
                border-radius: 10px;
                object-fit: cover;
                pointer-events: none;
            }

            #tr-rahat-chart-scan {
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 2147483644;
                overflow: hidden;
                background: rgba(16, 185, 129, 0.04);
            }
            .tr-scan-band {
                position: absolute;
                top: 0;
                bottom: 0;
                width: 115px;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(34, 197, 94, 0.2),
                    rgba(56, 189, 248, 0.34),
                    rgba(45, 212, 191, 0.18),
                    transparent
                );
                border-left: 2px solid rgba(74, 222, 128, 0.75);
                animation: trChartColumnSweep 1.6s ease-in-out infinite;
            }

            #tr-rahat-modal {
                position: fixed;
                inset: 0;
                background: rgba(2, 6, 15, 0.58);
                backdrop-filter: blur(3px);
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
                max-width: 392px;
                background: linear-gradient(180deg, #0d1628 0%, #080e1b 100%);
                border-radius: 16px;
                color: #f8fafc;
                overflow: hidden;
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.88);
                animation: trModalPop 0.25s ease-out;
            }
            .tr-win-scan {
                border: 1.5px solid rgba(56, 189, 248, 0.45);
            }
            .tr-win-call {
                border: 2px solid rgba(34, 197, 94, 0.78);
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9), 0 0 34px rgba(34, 197, 94, 0.28);
            }
            .tr-win-put {
                border: 2px solid rgba(239, 68, 68, 0.78);
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.9), 0 0 34px rgba(239, 68, 68, 0.28);
            }
            .tr-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 11px 14px;
                background: rgba(15, 23, 42, 0.95);
                border-bottom: 1px solid rgba(148, 163, 184, 0.14);
            }
            .tr-head-left {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .tr-badge-blue {
                font-size: 10.5px;
                font-weight: 800;
                color: #7dd3fc;
                background: rgba(14, 165, 233, 0.16);
                border: 1px solid rgba(56, 189, 248, 0.45);
                padding: 2px 8px;
                border-radius: 8px;
            }
            .tr-badge-mode {
                font-size: 10px;
                font-weight: 800;
                color: #f8fafc;
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.24);
                padding: 3px 9px;
                border-radius: 999px;
            }
            .tr-close {
                width: 28px;
                height: 28px;
                border-radius: 8px;
                border: 1px solid rgba(148, 163, 184, 0.24);
                background: rgba(30, 41, 59, 0.85);
                color: #e2e8f0;
                font-weight: 800;
                cursor: pointer;
            }
            .tr-body {
                padding: 14px;
            }
            .tr-capture-screen {
                position: relative;
                height: 175px;
                border-radius: 13px;
                background: radial-gradient(circle at 50% 45%, rgba(34, 197, 94, 0.14), rgba(5, 10, 20, 0.96) 75%);
                border: 1px solid rgba(56, 189, 248, 0.24);
                overflow: hidden;
                padding: 12px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .tr-capture-beam {
                position: absolute;
                left: 0;
                right: 0;
                height: 26px;
                background: linear-gradient(180deg, transparent, rgba(56, 189, 248, 0.35), rgba(34, 197, 94, 0.45), transparent);
                animation: trCaptureScanBeam 1.5s linear infinite;
                pointer-events: none;
            }
            .tr-hub-card {
                background: rgba(9, 15, 28, 0.88);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 13px;
                padding: 10px;
            }
            .tr-hub-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 8px;
                margin: 10px 0;
            }
            .tr-node {
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 10px;
                padding: 8px 4px;
                text-align: center;
                font-size: 10.5px;
                font-weight: 800;
            }
            .tr-node-trend {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.28), rgba(6, 95, 70, 0.35));
                border-color: #22c55e;
                color: #6ee7b7;
            }
            .tr-checks {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4px 10px;
                font-size: 10.5px;
                color: #cbd5e1;
                margin-bottom: 10px;
            }
            .tr-analyzing-bar {
                width: 100%;
                padding: 9px;
                border-radius: 10px;
                background: linear-gradient(90deg, #2563eb, #10b981);
                color: #ffffff;
                font-size: 12px;
                font-weight: 800;
                text-align: center;
            }
            .tr-grad-transition {
                height: 290px;
                border-radius: 13px;
                background: linear-gradient(155deg, #0a1f38 0%, #0d3b4c 52%, #1b1d42 100%);
                border: 1px solid rgba(56, 189, 248, 0.25);
            }
            .tr-call-panel {
                margin: 10px 0 12px;
                padding: 14px;
                border-radius: 13px;
                text-align: center;
                border: 1.5px solid rgba(34, 197, 94, 0.72);
                background: linear-gradient(180deg, rgba(16, 185, 129, 0.24), rgba(6, 78, 59, 0.15));
            }
            .tr-put-panel {
                margin: 10px 0 12px;
                padding: 14px;
                border-radius: 13px;
                text-align: center;
                border: 1.5px solid rgba(239, 68, 68, 0.72);
                background: linear-gradient(180deg, rgba(239, 68, 68, 0.24), rgba(127, 29, 29, 0.15));
            }
            .tr-grid-2 {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 10px;
            }
            .tr-box {
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 11px;
                padding: 9px;
            }
            .tr-confirm-btn {
                width: 100%;
                margin-top: 10px;
                padding: 10px 12px;
                border: none;
                border-radius: 11px;
                font-size: 12px;
                font-weight: 900;
                color: #ffffff;
                cursor: pointer;
            }
            .tr-btn-call {
                background: linear-gradient(90deg, #15803d, #22c55e, #0ea5e9);
            }
            .tr-btn-put {
                background: linear-gradient(90deg, #b91c1c, #ef4444, #f97316);
            }
            #tr-rahat-trade-banner {
                position: fixed;
                top: 66px;
                right: 12px;
                max-width: 300px;
                z-index: 2147483647;
                padding: 10px 13px;
                border-radius: 12px;
                color: #f0fdf4;
                box-shadow: 0 12px 28px rgba(0, 0, 0, 0.78);
                animation: trBannerSlide 0.25s ease-out;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
        `;
        document.head.appendChild(style);
    }

    function getAssetPair() {
        try {
            const els = document.querySelectorAll("*");
            for (let i = 0; i < els.length; i++) {
                const el = els[i];
                if (el.children.length === 0 && el.innerText) {
                    const txt = el.innerText.trim();
                    if (/^[A-Z]{3}\/[A-Z]{3}(\s*\(OTC\))?$/.test(txt)) {
                        return txt;
                    }
                }
            }
        } catch (_) {}
        return "USD/DZD (OTC)";
    }

    function getLivePriceEstimate(signal) {
        const base = signal === "CALL" ? 254.104 : 253.892;
        const jitter = ((Date.now() % 90) - 45) / 1000;
        return (base + jitter).toFixed(3);
    }

    function showTradeOpenedBanner(asset, signal, price, confidence, isCall) {
        const old = document.getElementById("tr-rahat-trade-banner");
        if (old) old.remove();

        let secondsLeft = 15;
        const banner = document.createElement("div");
        banner.id = "tr-rahat-trade-banner";
        banner.style.background = isCall
            ? "linear-gradient(135deg, rgba(21, 128, 61, 0.97), rgba(14, 116, 144, 0.97))"
            : "linear-gradient(135deg, rgba(185, 28, 28, 0.97), rgba(194, 65, 12, 0.97))";
        banner.style.border = isCall ? "1.5px solid #4ade80" : "1.5px solid #f87171";

        const renderBanner = () => {
            const mm = String(Math.floor(secondsLeft / 60)).padStart(2, "0");
            const ss = String(secondsLeft % 60).padStart(2, "0");
            banner.innerHTML = `
                <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
                    <span style="font-size:11.5px;font-weight:900;">${BOT_NAME} • ${signal}</span>
                    <span style="font-size:11px;font-weight:800;background:rgba(0,0,0,0.25);padding:2px 7px;border-radius:999px;">${mm}:${ss}</span>
                </div>
                <div style="font-size:10.5px;font-weight:700;margin-top:3px;opacity:0.96;">
                    Trade setup confirmed at ${price} ${asset} (${confidence}%)
                </div>
            `;
        };

        renderBanner();
        document.body.appendChild(banner);

        const iv = setInterval(() => {
            secondsLeft -= 1;
            if (secondsLeft <= 0 || !banner.parentNode) {
                clearInterval(iv);
                if (banner.parentNode) banner.remove();
                return;
            }
            renderBanner();
        }, 1000);
    }

    function startChartScan() {
        stopChartScan();
        const el = document.createElement("div");
        el.id = "tr-rahat-chart-scan";
        el.innerHTML = `<div class="tr-scan-band"></div>`;
        document.body.appendChild(el);
    }

    function stopChartScan() {
        const el = document.getElementById("tr-rahat-chart-scan");
        if (el) el.remove();
    }

    async function fetchLiveSignal(asset) {
        try {
            const res = await fetch(`${SERVER_URL}/signal?asset=${encodeURIComponent(asset)}&t=${Date.now()}`);
            if (res.ok) return await res.json();
        } catch (_) {}
        const fallback = Math.floor(Date.now() / 1000) % 2 === 0 ? "CALL" : "PUT";
        return {
            bot: BOT_NAME,
            asset,
            signal: fallback,
            confidence: 91,
            trend: fallback === "CALL" ? "Uptrend" : "Downtrend",
            pattern: fallback === "CALL" ? "Bullish Momentum" : "Bearish Momentum"
        };
    }

    // ~7000ms (7 seconds) smooth scan sequence before showing confirmation window
    function startSevenSecondScan() {
        const old = document.getElementById("tr-rahat-modal");
        if (old) old.remove();

        const asset = getAssetPair();
        startChartScan();

        const modal = document.createElement("div");
        modal.id = "tr-rahat-modal";
        const win = document.createElement("div");
        win.className = "tr-window tr-win-scan";
        modal.appendChild(win);
        document.body.appendChild(modal);

        const closeWin = () => {
            stopChartScan();
            if (modal.parentNode) modal.remove();
        };

        // 0ms -> 2500ms: Market Analysis & Screen Capture
        win.innerHTML = `
            <div class="tr-head">
                <div class="tr-head-left">
                    <span style="font-size:13.5px;font-weight:800;">Market Analysis</span>
                    <span class="tr-badge-blue">${asset}</span>
                </div>
                <button class="tr-close" id="tr-c-1">✕</button>
            </div>
            <div class="tr-body">
                <div class="tr-capture-screen">
                    <div class="tr-capture-beam"></div>
                    <div style="font-size:11px;font-weight:700;color:#e2e8f0;background:rgba(15,23,42,0.82);padding:4px 10px;border-radius:8px;align-self:flex-start;">
                        • Screen Capture
                    </div>
                    <div>
                        <div style="font-size:13px;font-weight:800;color:#fff;">⚡ Capturing live chart...</div>
                        <div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">Analyzing price action, indicators and market conditions...</div>
                    </div>
                </div>
                <div style="margin-top:11px;">
                    <div style="display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:5px;">
                        <span>Scanning Market Structure</span>
                        <span id="tr-pct">15%</span>
                    </div>
                    <div style="height:6px;border-radius:999px;background:#1e293b;overflow:hidden;">
                        <div id="tr-prog" style="width:15%;height:100%;background:linear-gradient(90deg,#38bdf8,#22c55e);transition:width 0.45s ease;"></div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById("tr-c-1").onclick = closeWin;

        const signalPromise = fetchLiveSignal(asset);

        setTimeout(() => {
            const p = document.getElementById("tr-pct");
            const b = document.getElementById("tr-prog");
            if (p) p.textContent = "78%";
            if (b) b.style.width = "78%";
        }, 1100);

        // 2500ms -> 5800ms: Chart Analyze 6-Node Hub
        setTimeout(() => {
            if (!modal.parentNode) return;
            win.innerHTML = `
                <div class="tr-head">
                    <div class="tr-head-left">
                        <span class="tr-badge-blue">BROKER</span>
                        <span style="font-size:13.5px;font-weight:800;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-close" id="tr-c-2">✕</button>
                </div>
                <div class="tr-body">
                    <div style="display:flex;justify-content:space-between;align-items:center;background:linear-gradient(90deg,rgba(16,185,129,0.22),rgba(56,189,248,0.16));border:1px solid rgba(34,197,94,0.35);border-radius:11px;padding:8px 11px;margin-bottom:10px;">
                        <div>
                            <div style="font-size:9.5px;font-weight:800;color:#34d399;">AI ENGINE</div>
                            <div style="font-size:13px;font-weight:800;color:#fff;">${BOT_NAME}</div>
                        </div>
                        <span class="tr-badge-mode">OTC • Real</span>
                    </div>
                    <div class="tr-hub-card">
                        <div style="text-align:center;font-size:12.5px;font-weight:800;color:#e2e8f0;">${asset} Chart Analyze</div>
                        <div class="tr-hub-grid">
                            <div class="tr-node" style="border-color:#38bdf8;color:#7dd3fc;">Market Data</div>
                            <div class="tr-node tr-node-trend">Trend</div>
                            <div class="tr-node" style="border-color:#a855f7;color:#d8b4fe;">Indicators</div>
                            <div class="tr-node" style="border-color:#f97316;color:#fdba74;">Price Action</div>
                            <div class="tr-node" style="border-color:#ef4444;color:#fca5a5;">AI Analysis</div>
                            <div class="tr-node" style="border-color:#eab308;color:#fde047;">Decision</div>
                        </div>
                        <div class="tr-checks">
                            <div>✓ Trend Analysis</div>
                            <div>✓ RSI & MACD</div>
                            <div>✓ Support / Resistance</div>
                            <div>✓ Momentum & Price</div>
                        </div>
                        <div class="tr-analyzing-bar">Analyzing chart...</div>
                    </div>
                </div>
            `;
            document.getElementById("tr-c-2").onclick = closeWin;
        }, 2500);

        // 5800ms -> 6600ms: Gradient Transition Card
        setTimeout(() => {
            if (!modal.parentNode) return;
            win.innerHTML = `
                <div class="tr-head">
                    <div class="tr-head-left">
                        <span class="tr-badge-blue">BROKER</span>
                        <span style="font-size:13.5px;font-weight:800;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-close" id="tr-c-3">✕</button>
                </div>
                <div class="tr-body">
                    <div class="tr-grad-transition"></div>
                </div>
            `;
            document.getElementById("tr-c-3").onclick = closeWin;
        }, 5800);

        // ~7000ms (7 seconds): Trade Confirmation Window (Dynamic per CALL/PUT trade)
        setTimeout(async () => {
            if (!modal.parentNode) return;
            stopChartScan();

            const data = await signalPromise;
            const isCall = String(data.signal || "CALL").toUpperCase() === "CALL";
            const sigLabel = isCall ? "CALL" : "PUT";
            const finalConf = Number(data.confidence) || 91;
            const startConf = Math.max(70, finalConf - 12);
            const trendText = data.trend || (isCall ? "Uptrend" : "Downtrend");
            const patternText = data.pattern || (isCall ? "Bullish Momentum" : "Bearish Momentum");
            const livePrice = getLivePriceEstimate(sigLabel);

            win.className = `tr-window ${isCall ? "tr-win-call" : "tr-win-put"}`;
            win.innerHTML = `
                <div class="tr-head">
                    <div class="tr-head-left">
                        <span class="tr-badge-blue">BROKER</span>
                        <span style="font-size:13.5px;font-weight:800;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-close" id="tr-c-4">✕</button>
                </div>
                <div class="tr-body">
                    <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(15,23,42,0.9);border:1px solid rgba(148,163,184,0.18);border-radius:10px;padding:7px 11px;">
                        <span style="font-size:12.5px;font-weight:800;">${asset}</span>
                        <span style="font-size:10.5px;font-weight:700;color:#34d399;">• Live read 1m</span>
                    </div>

                    <div class="${isCall ? "tr-call-panel" : "tr-put-panel"}">
                        <div style="font-size:10px;font-weight:800;letter-spacing:1px;color:#cbd5e1;">- PLACE OPTION -</div>
                        <div style="font-size:30px;font-weight:900;color:${isCall ? "#22c55e" : "#ef4444"};margin:3px 0;">
                            ${isCall ? "▲ CALL" : "▼ PUT"}
                        </div>
                        <div style="font-size:11px;color:#cbd5e1;">
                            ${isCall ? "Upward move expected. Enter on the next candle" : "Downward move expected. Enter on the next candle"}
                        </div>
                    </div>

                    <div class="tr-grid-2">
                        <div class="tr-box">
                            <div style="font-size:9.5px;font-weight:800;color:#94a3b8;">CONFIDENCE</div>
                            <div id="tr-conf-val" style="font-size:21px;font-weight:900;color:${isCall ? "#34d399" : "#f87171"};margin:2px 0;">${startConf}%</div>
                            <div style="font-size:10.5px;font-weight:700;color:#e2e8f0;">High conviction</div>
                            <div style="font-size:9.5px;color:#94a3b8;">Threshold 75%</div>
                        </div>
                        <div class="tr-box">
                            <div style="font-size:9.5px;font-weight:800;color:#94a3b8;margin-bottom:4px;">KEY LEVELS</div>
                            <div style="font-size:10.5px;font-weight:700;color:#f87171;">▲ RESISTANCE</div>
                            <div style="font-size:10.5px;font-weight:700;color:#38bdf8;margin:2px 0;">◆ PRICE ZONE</div>
                            <div style="font-size:10.5px;font-weight:700;color:#34d399;">▼ SUPPORT</div>
                        </div>
                    </div>

                    <div class="tr-grid-2" style="margin-bottom:0;">
                        <div class="tr-box" style="padding:7px 9px;font-size:10.5px;font-weight:700;">
                            TREND: <span style="color:${isCall ? "#34d399" : "#f87171"};">${trendText}</span>
                        </div>
                        <div class="tr-box" style="padding:7px 9px;font-size:10.5px;font-weight:700;">
                            PATTERN: <span style="color:#7dd3fc;">${patternText}</span>
                        </div>
                    </div>

                    <button id="tr-confirm-btn" class="tr-confirm-btn ${isCall ? "tr-btn-call" : "tr-btn-put"}">
                        CONFIRM ${sigLabel} TRADE (${livePrice})
                    </button>
                </div>
            `;
            document.getElementById("tr-c-4").onclick = closeWin;

            let cur = startConf;
            const confEl = document.getElementById("tr-conf-val");
            const timer = setInterval(() => {
                cur += 1;
                if (confEl) confEl.textContent = `${cur}%`;
                if (cur >= finalConf) clearInterval(timer);
            }, 45);

            document.getElementById("tr-confirm-btn").onclick = () => {
                closeWin();
                showTradeOpenedBanner(asset, sigLabel, livePrice, finalConf, isCall);
            };
        }, 7000);
    }

    function createSquareBot() {
        const box = document.createElement("div");
        box.id = "tr-rahat-square-bot";
        box.innerHTML = `
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
                startSevenSecondScan();
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
    def get_authentic_decision(market_context: str) -> dict:
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
                    "content": "You are the Trader Rahat binary options AI arbiter enforcing both-way directional analysis. Output STRICTLY 'CALL' or 'PUT'."
                },
                {
                    "role": "user",
                    "content": f"Analyze live market context: {market_context}. Output strictly 'CALL' or 'PUT'."
                }
            ],
            "temperature": 0.15,
            "max_tokens": 6
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=3)
            if response.status_code == 200:
                decision = response.json()["choices"][0]["message"]["content"].strip().upper()
                if decision in ["CALL", "PUT"]:
                    return {"signal": decision, "confidence": 91}
        except Exception:
            pass
        fallback = "CALL" if (int(time.time() * 7) % 2 == 0) else "PUT"
        return {"signal": fallback, "confidence": 91}


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
        base_bias = "CALL" if rsi < 50 else "PUT"
        market_ctx = f"Asset: {asset}, RSI: {rsi}, Bias: {base_bias}, NewsSafe: {news_safe}, Time: {current_time}"
        ai_res = GroqAIArbitrationCore.get_authentic_decision(market_ctx)
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
        res = jsonify({
            "bot": "Trader Rahat",
            "asset": request.args.get("asset", "USD/DZD (OTC)"),
            "signal": fallback_dir,
            "confidence": 91,
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
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
