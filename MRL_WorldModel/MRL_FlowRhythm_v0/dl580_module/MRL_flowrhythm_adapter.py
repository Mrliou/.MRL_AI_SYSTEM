"""
MRL FlowRhythm 模組 · DL580 本機載體（adapter）
origin_signature: MrLiouWord ｜ Additive-Only ｜ 本體 flow_rhythm.py（權威）不改一字

位置：本體或載體？→ 載體。承載本體 Jump → Collapse → Trace → Replay 全程，於母體本機提供 HTTP 入口。
對應段：run = Jump→Collapse→Trace；replay = Replay。
驗收語料：lexicon\\ 8 份原檔皆由母體 D:\\ 既有位置複製，SHA-256 與 lexicon\\SOURCES.sha256 逐一相符。

規格（與 MRL_Module_Integration_20261001_R06 同型）：
- 只聽 127.0.0.1:<port>，所有 /api/* 需 Authorization: Bearer <private\\flowrhythm.token>
- POST /api/flowrhythm/run      body: 粒子語句 .fltnz 純文字；?sandbox=1 才允許 provisional 映射
- POST /api/flowrhythm/replay   body: v0.2.0 軌跡純文字；回 byte_identical、封包雜湊
- GET  /health                  免驗證；只回版本與帳本長度
- GET  /api/flowrhythm/timeline 帳本（append-only JSONL，SHA-256 前序鏈）
- GET  /api/flowrhythm/verify   驗證帳本鏈
只用 Python 標準函式庫。
"""
import hashlib
import json
import re
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flow_rhythm as F  # noqa: E402

PORT = int(os.environ.get("MRL_FLOWRHYTHM_PORT", "7827"))
TOKEN_PATH = os.path.join(HERE, "private", "flowrhythm.token")
LEDGER = os.path.join(HERE, "runtime", "ledger.jsonl")
MAX_BODY = 32 * 1024
_lock = threading.Lock()


def _token():
    with open(TOKEN_PATH, encoding="utf-8") as f:
        return f.read().strip()


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _last_hash():
    if not os.path.exists(LEDGER):
        return "0" * 64
    last = None
    with open(LEDGER, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line
    return json.loads(last)["event_hash"] if last else "0" * 64


def _append(ev):
    with _lock:
        ev["previous_hash"] = _last_hash()
        body = json.dumps({k: v for k, v in ev.items() if k != "event_hash"}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ev["event_hash"] = _sha(ev["previous_hash"] + body)
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    return ev["event_hash"]


def verify_ledger():
    prev, n = "0" * 64, 0
    if not os.path.exists(LEDGER):
        return {"ok": True, "events": 0}
    with open(LEDGER, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            ev = json.loads(line)
            body = json.dumps({k: v for k, v in ev.items() if k != "event_hash"}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            if ev["previous_hash"] != prev or ev["event_hash"] != _sha(prev + body):
                return {"ok": False, "events": n, "broken_at": n}
            prev, n = ev["event_hash"], n + 1
    return {"ok": True, "events": n, "head": prev}


L = F.load_lexicon(os.path.join(HERE, "lexicon"))


class H(BaseHTTPRequestHandler):
    server_version = "MRL_FlowRhythm_Adapter/0.2.0"

    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _auth(self):
        a = self.headers.get("Authorization", "")
        return a.startswith("Bearer ") and a[7:].strip() == _token()

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            return self._json(200, {"service": "MRL_FlowRhythm_Module", "engine_version": F.ENGINE_VERSION,
                                    "origin_signature": F.SIGN, "ledger_events": verify_ledger().get("events", 0)})
        if not self._auth():
            return self._json(401, {"error": "unauthorized"})
        if u.path == "/api/flowrhythm/verify":
            return self._json(200, verify_ledger())
        if u.path == "/api/flowrhythm/timeline":
            rows = []
            if os.path.exists(LEDGER):
                with open(LEDGER, encoding="utf-8") as f:
                    rows = [json.loads(l) for l in f if l.strip()]
            return self._json(200, {"events": rows[-100:], "total": len(rows)})
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        if not self._auth():
            return self._json(401, {"error": "unauthorized"})
        n = int(self.headers.get("Content-Length", "0"))
        if n > MAX_BODY:
            return self._json(413, {"error": "body too large"})
        text = self.rfile.read(n).decode("utf-8")
        q = parse_qs(u.query)
        sandbox = q.get("sandbox", ["0"])[0] == "1"
        title = q.get("title", ["語場節奏"])[0]
        t0 = time.time()
        try:
            if u.path == "/api/flowrhythm/run":
                chain = F.chain_from_fltnz(text)
                r = F.run(chain, L, title=title, allow_provisional=sandbox)
                out = {"ok": True, "mode": "run", "chain_len": len(chain), "semantic_status": r["semantic_status"],
                       "provisional_mappings": r["provisional_mappings"], "final_sha256": r["final_sha256"],
                       "packets": r["field"]["packets"], "trace_fltnz": r["trace_fltnz"], "narration": r["narration"]}
            elif u.path == "/api/flowrhythm/replay":
                m = re.match(r"^# (.*?) · FlowRhythm v", text.split("\n", 1)[0])
                r = F.replay(text, L, title=(m.group(1) if m else title), allow_provisional=sandbox)
                out = {"ok": True, "mode": "replay", "byte_identical": r["trace_fltnz"] == text, "trace_ops": r["trace_ops"],
                       "semantic_status": r["semantic_status"], "final_sha256": r["final_sha256"], "packets": r["field"]["packets"]}
            else:
                return self._json(404, {"error": "not found"})
            code = 200
        except F.ProvisionalSemanticMappingError as e:
            out, code = {"ok": False, "error": "provisional_semantic_mapping", "detail": str(e)}, 422
        except F.SemanticAuthorityIntegrityError as e:
            out, code = {"ok": False, "error": "semantic_authority_integrity", "detail": str(e)}, 422
        except Exception as e:  # noqa: BLE001
            out, code = {"ok": False, "error": type(e).__name__, "detail": str(e)}, 400
        eh = _append({"module_id": "flowrhythm", "mode": u.path.rsplit("/", 1)[-1], "sandbox": sandbox,
                      "input_sha256": _sha(text), "status": "completed" if out.get("ok") else "failed",
                      "final_sha256": out.get("final_sha256"), "duration_ms": round((time.time() - t0) * 1000, 2),
                      "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "origin_signature": F.SIGN,
                      "release": "20261004-R01"})
        out["event_hash"] = eh
        return self._json(code, out)

    def log_message(self, *a):  # 安靜
        pass


if __name__ == "__main__":
    if not os.path.exists(TOKEN_PATH):
        raise SystemExit("missing private/flowrhythm.token")
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    print(f"MRL_FlowRhythm_Module listening 127.0.0.1:{PORT}", flush=True)
    srv.serve_forever()
