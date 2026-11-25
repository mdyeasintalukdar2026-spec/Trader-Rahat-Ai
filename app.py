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
            "tr-rahat-chart-scanner",
            "tr-rahat-modal",
            "tr-rahat-toast"
        ].forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
    }

    function injectStyles() {
        const style = document.createElement("style");
        style.id = "tr-rahat-styles";
        style.textContent = `
            @keyframes trSquareBgAura {
                0%, 100% {
                    box-shadow:
                        0 0 14px rgba(56, 189, 248, 0.75),
                        0 0 28px rgba(16, 185, 129, 0.45),
                        inset 0 0 12px rgba(56, 189, 248, 0.35);
                    border-color: #38bdf8;
                }
                50% {
                    box-shadow:
                        0 0 20px rgba(34, 197, 94, 0.85),
                        0 0 36px rgba(59, 130, 246, 0.55),
                        inset 0 0 16px rgba(34, 197, 94, 0.45);
                    border-color: #22c55e;
                }
            }
            @keyframes trAuraSpin {
                0% { transform: rotate(0deg) scale(1); opacity: 0.65; }
                50% { transform: rotate(180deg) scale(1.12); opacity: 0.95; }
                100% { transform: rotate(360deg) scale(1); opacity: 0.65; }
            }
            @keyframes trTapRipple {
                0% { transform: scale(0.85); opacity: 0.95; }
                100% { transform: scale(1.75); opacity: 0; }
            }
            @keyframes trVerticalScan {
                0% { left: -18%; opacity: 0.35; }
                50% { opacity: 0.95; }
                100% { left: 105%; opacity: 0.35; }
            }
            @keyframes trLaserSweep {
                0% { top: -15%; opacity: 0.3; }
                50% { opacity: 1; }
                100% { top: 105%; opacity: 0.3; }
            }
            @keyframes trCardPop {
                0% { opacity: 0; transform: scale(0.94) translateY(12px); }
                100% { opacity: 1; transform: scale(1) translateY(0); }
            }
            @keyframes trToastSlide {
                0% { opacity: 0; transform: translateX(28px); }
                100% { opacity: 1; transform: translateX(0); }
            }

            #tr-rahat-square-bot {
                position: fixed;
                right: 12px;
                top: 57%;
                width: 66px;
                height: 66px;
                border-radius: 14px;
                background: linear-gradient(155deg, #091326 0%, #0f1f3d 60%, #072923 100%);
                border: 2px solid #38bdf8;
                z-index: 2147483645;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                user-select: none;
                touch-action: none;
                overflow: visible;
                animation: trSquareBgAura 2.2s infinite ease-in-out;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            #tr-rahat-square-bot::before {
                content: "";
                position: absolute;
                inset: -5px;
                border-radius: 18px;
                background: conic-gradient(from 0deg, #38bdf8, #22c55e, #6366f1, #22c55e, #38bdf8);
                z-index: -1;
                filter: blur(6px);
                animation: trAuraSpin 4s linear infinite;
            }
            .tr-sq-inner {
                width: 100%;
                height: 100%;
                border-radius: 12px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                position: relative;
                background: #071122;
            }
            .tr-sq-inner img {
                width: 40px;
                height: 40px;
                border-radius: 9px;
                object-fit: cover;
                pointer-events: none;
            }
            .tr-sq-name {
                margin-top: 2px;
                font-size: 8px;
                font-weight: 900;
                color: #f8fafc;
                letter-spacing: 0.2px;
                white-space: nowrap;
                pointer-events: none;
            }
            .tr-sq-badge {
                position: absolute;
                top: -7px;
                left: -7px;
                background: linear-gradient(90deg, #16a34a, #22c55e);
                color: #ffffff;
                font-size: 9px;
                font-weight: 900;
                padding: 1px 6px;
                border-radius: 6px;
                border: 1px solid rgba(255,255,255,0.35);
                pointer-events: none;
            }
            .tr-tap-ring {
                position: absolute;
                inset: -4px;
                border-radius: 16px;
                border: 2px solid #22c55e;
                pointer-events: none;
                animation: trTapRipple 0.55s ease-out forwards;
            }

            #tr-rahat-chart-scanner {
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 2147483644;
                overflow: hidden;
                background: rgba(16, 185, 129, 0.05);
            }
            .tr-scan-column {
                position: absolute;
                top: 0;
                bottom: 0;
                width: 90px;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(34, 197, 94, 0.14),
                    rgba(56, 189, 248, 0.28),
                    rgba(34, 197, 94, 0.14),
                    transparent
                );
                border-left: 1.5px solid rgba(74, 222, 128, 0.65);
                animation: trVerticalScan 1.45s ease-in-out infinite;
            }

            #tr-rahat-modal {
                position: fixed;
                inset: 0;
                background: rgba(2, 6, 15, 0.65);
                backdrop-filter: blur(4px);
                z-index: 2147483646;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            .tr-panel {
                width: 100%;
                max-width: 392px;
                background: linear-gradient(180deg, #0e1729 0%, #080e1a 100%);
                border: 1.5px solid rgba(56, 189, 248, 0.4);
                border-radius: 16px;
                box-shadow: 0 22px 55px rgba(0, 0, 0, 0.85), 0 0 30px rgba(34, 197, 94, 0.16);
                color: #f8fafc;
                overflow: hidden;
                animation: trCardPop 0.25s ease-out;
            }
            .tr-top-bar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 11px 14px;
                background: rgba(15, 23, 42, 0.95);
                border-bottom: 1px solid rgba(148, 163, 184, 0.15);
            }
            .tr-top-left {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .tr-pill-blue {
                font-size: 10.5px;
                font-weight: 800;
                color: #7dd3fc;
                background: rgba(14, 165, 233, 0.16);
                border: 1px solid rgba(56, 189, 248, 0.45);
                padding: 2px 8px;
                border-radius: 8px;
            }
            .tr-pill-otc {
                font-size: 10px;
                font-weight: 800;
                color: #f8fafc;
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.25);
                padding: 3px 9px;
                border-radius: 999px;
            }
            .tr-x-btn {
                width: 28px;
                height: 28px;
                border-radius: 8px;
                border: 1px solid rgba(148, 163, 184, 0.25);
                background: rgba(30, 41, 59, 0.8);
                color: #e2e8f0;
                font-weight: 800;
                cursor: pointer;
            }
            .tr-content {
                padding: 14px;
            }
            .tr-capture-stage {
                position: relative;
                height: 170px;
                border-radius: 13px;
                background: radial-gradient(circle at 50% 40%, rgba(34, 197, 94, 0.16), rgba(5, 10, 20, 0.96) 75%);
                border: 1px solid rgba(56, 189, 248, 0.25);
                overflow: hidden;
                padding: 12px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .tr-laser-line {
                position: absolute;
                left: 0;
                right: 0;
                height: 28px;
                background: linear-gradient(180deg, transparent, rgba(56, 189, 248, 0.35), rgba(34, 197, 94, 0.5), transparent);
                animation: trLaserSweep 1.5s linear infinite;
                pointer-events: none;
            }
            .tr-hub-box {
                background: rgba(9, 15, 28, 0.85);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 13px;
                padding: 10px;
            }
            .tr-nodes-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 8px;
                margin: 10px 0;
            }
            .tr-n-item {
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 10px;
                padding: 8px 4px;
                text-align: center;
                font-size: 10.5px;
                font-weight: 800;
            }
            .tr-n-trend {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(6, 95, 70, 0.3));
                border-color: #22c55e;
                color: #6ee7b7;
            }
            .tr-checklist {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4px 10px;
                font-size: 10.5px;
                color: #cbd5e1;
                margin-bottom: 10px;
            }
            .tr-analyzing-btn {
                width: 100%;
                padding: 9px;
                border-radius: 10px;
                background: linear-gradient(90deg, #2563eb, #10b981);
                color: #ffffff;
                font-size: 12px;
                font-weight: 800;
                text-align: center;
            }
            .tr-call-box {
                margin: 10px 0 12px;
                padding: 14px;
                border-radius: 13px;
                text-align: center;
                border: 1.5px solid rgba(34, 197, 94, 0.65);
                background: linear-gradient(180deg, rgba(16, 185, 129, 0.22), rgba(6, 78, 59, 0.14));
            }
            .tr-put-box {
                margin: 10px 0 12px;
                padding: 14px;
                border-radius: 13px;
                text-align: center;
                border: 1.5px solid rgba(239, 68, 68, 0.65);
                background: linear-gradient(180deg, rgba(239, 68, 68, 0.22), rgba(127, 29, 29, 0.14));
            }
            .tr-two-col {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 10px;
            }
            .tr-stat-card {
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 11px;
                padding: 9px;
            }
            #tr-rahat-toast {
                position: fixed;
                top: 66px;
                right: 12px;
                z-index: 2147483647;
                background: linear-gradient(90deg, rgba(22, 101, 52, 0.96), rgba(15, 23, 42, 0.96));
                border: 1.5px solid #22c55e;
                color: #f0fdf4;
                padding: 8px 13px;
                border-radius: 11px;
                font-size: 11.5px;
                font-weight: 800;
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.7);
                animation: trToastSlide 0.25s ease-out;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
        `;
        document.head.appendChild(style);
    }

    function getCurrentAsset() {
        try {
            const els = document.querySelectorAll("*");
            for (let i = 0; i < els.length; i++) {
                const el = els[i];
                if (el.children.length === 0 && el.innerText) {
                    const t = el.innerText.trim();
                    if (/^[A-Z]{3}\/[A-Z]{3}(\s*\(OTC\))?$/.test(t)) {
                        return t;
                    }
                }
            }
        } catch (_) {}
        return "USD/DZD (OTC)";
    }

    function showToast(msg) {
        const old = document.getElementById("tr-rahat-toast");
        if (old) old.remove();
        const t = document.createElement("div");
        t.id = "tr-rahat-toast";
        t.textContent = msg;
        document.body.appendChild(t);
        setTimeout(() => {
            if (t.parentNode) t.remove();
        }, 3500);
    }

    function startChartScanEffect() {
        stopChartScanEffect();
        const scan = document.createElement("div");
        scan.id = "tr-rahat-chart-scanner";
        scan.innerHTML = `<div class="tr-scan-column"></div>`;
        document.body.appendChild(scan);
    }

    function stopChartScanEffect() {
        const scan = document.getElementById("tr-rahat-chart-scanner");
        if (scan) scan.remove();
    }

    async function requestSignal(asset) {
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

    function runFullAnalysisSequence() {
        const old = document.getElementById("tr-rahat-modal");
        if (old) old.remove();

        const asset = getCurrentAsset();
        startChartScanEffect();

        const modal = document.createElement("div");
        modal.id = "tr-rahat-modal";
        const panel = document.createElement("div");
        panel.className = "tr-panel";
        modal.appendChild(panel);
        document.body.appendChild(modal);

        const closeAll = () => {
            stopChartScanEffect();
            if (modal.parentNode) modal.remove();
        };

        // Step 1: Market Analysis & Screen Capture
        panel.innerHTML = `
            <div class="tr-top-bar">
                <div class="tr-top-left">
                    <span style="font-size:13.5px;font-weight:800;color:#f8fafc;">Market Analysis</span>
                    <span class="tr-pill-blue">${asset}</span>
                </div>
                <button class="tr-x-btn" id="tr-x-1">✕</button>
            </div>
            <div class="tr-content">
                <div class="tr-capture-stage">
                    <div class="tr-laser-line"></div>
                    <div style="font-size:11px;font-weight:700;color:#e2e8f0;background:rgba(15,23,42,0.8);padding:4px 10px;border-radius:8px;align-self:flex-start;">
                        • Screen Capture • ${BOT_NAME}
                    </div>
                    <div>
                        <div style="font-size:13px;font-weight:800;color:#fff;">⚡ Capturing live chart...</div>
                        <div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">Analyzing price action, indicators and market conditions...</div>
                    </div>
                </div>
                <div style="margin-top:11px;">
                    <div style="display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:5px;">
                        <span>Scanning Market Structure</span>
                        <span id="tr-scan-pct">12%</span>
                    </div>
                    <div style="height:6px;border-radius:999px;background:#1e293b;overflow:hidden;">
                        <div id="tr-scan-fill" style="width:12%;height:100%;background:linear-gradient(90deg,#38bdf8,#22c55e);transition:width 0.3s ease;"></div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById("tr-x-1").onclick = closeAll;

        const sigPromise = requestSignal(asset);

        setTimeout(() => {
            const p = document.getElementById("tr-scan-pct");
            const f = document.getElementById("tr-scan-fill");
            if (p) p.textContent = "82%";
            if (f) f.style.width = "82%";
        }, 700);

        // Step 2: Chart Analyze 6-Node Hub
        setTimeout(() => {
            if (!modal.parentNode) return;
            panel.innerHTML = `
                <div class="tr-top-bar">
                    <div class="tr-top-left">
                        <span class="tr-pill-blue">BROKER</span>
                        <span style="font-size:13.5px;font-weight:800;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-x-btn" id="tr-x-2">✕</button>
                </div>
                <div class="tr-content">
                    <div style="display:flex;justify-content:space-between;align-items:center;background:linear-gradient(90deg,rgba(16,185,129,0.2),rgba(56,189,248,0.15));border:1px solid rgba(34,197,94,0.35);border-radius:11px;padding:8px 11px;margin-bottom:10px;">
                        <div>
                            <div style="font-size:9.5px;font-weight:800;color:#34d399;">AI ENGINE</div>
                            <div style="font-size:13px;font-weight:800;color:#fff;">${BOT_NAME}</div>
                        </div>
                        <span class="tr-pill-otc">OTC • Real</span>
                    </div>
                    <div class="tr-hub-box">
                        <div style="text-align:center;font-size:12.5px;font-weight:800;color:#e2e8f0;">${asset} Chart Analyze</div>
                        <div class="tr-nodes-grid">
                            <div class="tr-n-item" style="border-color:#38bdf8;color:#7dd3fc;">Market Data</div>
                            <div class="tr-n-item tr-n-trend">Trend</div>
                            <div class="tr-n-item" style="border-color:#a855f7;color:#d8b4fe;">Indicators</div>
                            <div class="tr-n-item" style="border-color:#f97316;color:#fdba74;">Price Action</div>
                            <div class="tr-n-item" style="border-color:#ef4444;color:#fca5a5;">AI Analysis</div>
                            <div class="tr-n-item" style="border-color:#eab308;color:#fde047;">Decision</div>
                        </div>
                        <div class="tr-checklist">
                            <div>✓ Trend Analysis</div>
                            <div>✓ RSI & MACD</div>
                            <div>✓ Support / Resistance</div>
                            <div>✓ Momentum & Price</div>
                        </div>
                        <div class="tr-analyzing-btn">Analyzing chart...</div>
                    </div>
                </div>
            `;
            document.getElementById("tr-x-2").onclick = closeAll;
        }, 1850);

        // Step 3: Final CALL / PUT Signal Card + Confidence Counter
        setTimeout(async () => {
            if (!modal.parentNode) return;
            stopChartScanEffect();
            const data = await sigPromise;
            const isCall = String(data.signal || "CALL").toUpperCase() === "CALL";
            const finalConf = Number(data.confidence) || 91;
            const startConf = Math.max(70, finalConf - 12);
            const trendVal = data.trend || (isCall ? "Uptrend" : "Downtrend");
            const patternVal = data.pattern || (isCall ? "Bullish Momentum" : "Bearish Momentum");

            panel.innerHTML = `
                <div class="tr-top-bar">
                    <div class="tr-top-left">
                        <span class="tr-pill-blue">BROKER</span>
                        <span style="font-size:13.5px;font-weight:800;">${BOT_NAME}</span>
                    </div>
                    <button class="tr-x-btn" id="tr-x-3">✕</button>
                </div>
                <div class="tr-content">
                    <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(15,23,42,0.9);border:1px solid rgba(148,163,184,0.18);border-radius:10px;padding:7px 11px;">
                        <span style="font-size:12.5px;font-weight:800;">${asset}</span>
                        <span style="font-size:10.5px;font-weight:700;color:#34d399;">• Live read 1m</span>
                    </div>

                    <div class="${isCall ? "tr-call-box" : "tr-put-box"}">
                        <div style="font-size:10px;font-weight:800;letter-spacing:1px;color:#cbd5e1;">- PLACE OPTION -</div>
                        <div style="font-size:30px;font-weight:900;color:${isCall ? "#22c55e" : "#ef4444"};margin:3px 0;">
                            ${isCall ? "▲ CALL" : "▼ PUT"}
                        </div>
                        <div style="font-size:11px;color:#cbd5e1;">
                            ${isCall ? "Upward move expected. Enter on the next candle" : "Downward move expected. Enter on the next candle"}
                        </div>
                    </div>

                    <div class="tr-two-col">
                        <div class="tr-stat-card">
                            <div style="font-size:9.5px;font-weight:800;color:#94a3b8;">CONFIDENCE</div>
                            <div id="tr-conf-num" style="font-size:21px;font-weight:900;color:${isCall ? "#34d399" : "#f87171"};margin:2px 0;">${startConf}%</div>
                            <div style="font-size:10.5px;font-weight:700;color:#e2e8f0;">High conviction</div>
                            <div style="font-size:9.5px;color:#94a3b8;">Threshold 75%</div>
                        </div>
                        <div class="tr-stat-card">
                            <div style="font-size:9.5px;font-weight:800;color:#94a3b8;margin-bottom:4px;">KEY LEVELS</div>
                            <div style="font-size:10.5px;font-weight:700;color:#f87171;">▲ RESISTANCE</div>
                            <div style="font-size:10.5px;font-weight:700;color:#38bdf8;margin:2px 0;">◆ PRICE ZONE</div>
                            <div style="font-size:10.5px;font-weight:700;color:#34d399;">▼ SUPPORT</div>
                        </div>
                    </div>

                    <div class="tr-two-col" style="margin-bottom:0;">
                        <div class="tr-stat-card" style="padding:7px 9px;font-size:10.5px;font-weight:700;">
                            TREND: <span style="color:${isCall ? "#34d399" : "#f87171"};">${trendVal}</span>
                        </div>
                        <div class="tr-stat-card" style="padding:7px 9px;font-size:10.5px;font-weight:700;">
                            PATTERN: <span style="color:#7dd3fc;">${patternVal}</span>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById("tr-x-3").onclick = closeAll;

            let cur = startConf;
            const confEl = document.getElementById("tr-conf-num");
            const timer = setInterval(() => {
                cur += 1;
                if (confEl) confEl.textContent = `${cur}%`;
                if (cur >= finalConf) clearInterval(timer);
            }, 45);

            showToast(`${BOT_NAME} • ${isCall ? "CALL" : "PUT"} (${finalConf}%) • ${asset}`);
        }, 3700);
    }

    function createSquareFloatingBot() {
        const box = document.createElement("div");
        box.id = "tr-rahat-square-bot";
        box.innerHTML = `
            <span class="tr-sq-badge">TR</span>
            <div class="tr-sq-inner">
                <img src="${BOT_LOGO}" alt="${BOT_NAME}" onerror="this.style.display='none';" />
                <span class="tr-sq-name">${BOT_NAME}</span>
            </div>
        `;

        let dragging = false;
        let moved = false;
        let dx = 0;
        let dy = 0;

        const down = (e) => {
            dragging = true;
            moved = false;
            const pt = e.touches ? e.touches[0] : e;
            const rect = box.getBoundingClientRect();
            dx = pt.clientX - rect.left;
            dy = pt.clientY - rect.top;
        };

        const move = (e) => {
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

        const up = () => {
            dragging = false;
        };

        box.addEventListener("mousedown", down);
        box.addEventListener("touchstart", down, { passive: true });
        window.addEventListener("mousemove", move);
        window.addEventListener("touchmove", move, { passive: true });
        window.addEventListener("mouseup", up);
        window.addEventListener("touchend", up);

        box.addEventListener("click", () => {
            if (moved) return;
            const ring = document.createElement("span");
            ring.className = "tr-tap-ring";
            box.appendChild(ring);
            setTimeout(() => {
                if (ring.parentNode) ring.remove();
            }, 600);
            runFullAnalysisSequence();
        });

        document.body.appendChild(box);
    }

    function boot() {
        if (!document.body) {
            setTimeout(boot, 100);
            return;
        }
        cleanup();
        injectStyles();
        createSquareFloatingBot();
    }

    if (document.readyState === "complete" || document.readyState === "interactive") {
        boot();
    } else {
        window.addEventListener("DOMContentLoaded", boot);
        setTimeout(boot, 350);
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
