"""
FlowRhythm 模組 · 母體實機自檢（6 顆母體種子，同 tests/test_rhythm.py E 段）
origin_signature: MrLiouWord
1. lexicon\\ 8 份原檔 SHA-256 與 SOURCES.sha256 逐一相符（來源：母體 D:\\ 既有位置）
2. 本體直跑：6 顆種子 run → replay 逐位元組重現；固定時鐘下封包雜湊與雲端載體參考值一致
3. 經 127.0.0.1:7827 載體：EchoPersona 軌跡 replay byte_identical；正典 run 拒絕 provisional；帳本鏈 verify
輸出：MRL_selftest_receipt.json（只新增）
"""
import hashlib, io, json, os, sys, time, urllib.request, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import flow_rhythm as F
LEX = os.path.join(HERE, "lexicon"); L = F.load_lexicon(LEX)
FIX = "2025-07-23T19:41:36.746707Z"
# 雲端載體（mrliousilly / particle-replay）實測過的固定時鐘封包雜湊，EchoPersona.pcode = 0a9f53a15181931d
REF_EP_PREFIX = "0a9f53a15181931d"
res = {"origin_signature": F.SIGN, "engine_version": F.ENGINE_VERSION, "release": "20261004-R01",
       "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "host": os.environ.get("COMPUTERNAME"), "checks": {}}

# 1
ok = True; src = {}
for line in open(os.path.join(LEX, "SOURCES.sha256"), encoding="utf-8"):
    h, name = line.rstrip("\n").split("  ", 1)
    p = os.path.join(LEX, name); got = hashlib.sha256(open(p, "rb").read()).hexdigest()
    src[name] = got == h; ok &= got == h
res["checks"]["1_lexicon_sources_sha256"] = ok; res["lexicon_sources"] = src

# 2
seeds = []
for n in ("下載 EchoPersona.pcode", "下載 EchoPersona.Sample.v1.flpkg", "下載 FluinCoreSeed.v1.flseed", "下載 Memory.Seed.Core.v1.flseed"):
    ch, _ = F.load_seed(os.path.join(LEX, n), L); seeds.append((n.replace("下載 ", ""), ch))
with zipfile.ZipFile(os.path.join(LEX, "重新下載 FluinSim.DualSet.v1.flsim")) as z:
    for g in ("Group1_EchoPersona", "Group2_ConflictChange"):
        seeds.append((g, F.chain_from_fltnz(z.read(g + ".fltnz").decode("utf-8"))))
runs = []; all_ok = True; ep_trace = None
for name, ch in seeds:
    r = F.run(ch, L, F.Clock(FIX), name, allow_provisional=True)
    rp = F.replay(r["trace_fltnz"], L, name, allow_provisional=True)
    good = rp["trace_fltnz"] == r["trace_fltnz"] and rp["final_sha256"] == r["final_sha256"]
    all_ok &= good
    runs.append({"seed": name, "particles": len(ch), "final_sha256": r["final_sha256"], "replay_byte_identical": good})
    if name == "EchoPersona.pcode": ep_trace = r["trace_fltnz"]; ep_hash = r["final_sha256"]
res["checks"]["2_six_seeds_run_replay_byte_identical"] = all_ok
res["checks"]["2_echopersona_packet_matches_cloud_carrier"] = ep_hash.startswith(REF_EP_PREFIX)
res["seeds"] = runs

# 3 via adapter
tok = open(os.path.join(HERE, "private", "flowrhythm.token"), encoding="utf-8").read().strip()
def call(path, body=None, method="POST"):
    req = urllib.request.Request("http://127.0.0.1:7827" + path, data=body.encode("utf-8") if body is not None else None, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read().decode("utf-8") or "{}")
s, h = call("/health", method="GET"); res["adapter_health"] = h
s1, j1 = call("/api/flowrhythm/replay?sandbox=1", ep_trace)
res["checks"]["3_adapter_replay_echopersona_byte_identical"] = s1 == 200 and j1.get("byte_identical") is True and j1.get("final_sha256") == ep_hash
s2, j2 = call("/api/flowrhythm/run", "\n".join(seeds[4][1]))  # Group1 正典 → 應拒絕
res["checks"]["3_adapter_canonical_rejects_provisional"] = s2 == 422 and j2.get("error") == "provisional_semantic_mapping"
s3, j3 = call("/api/flowrhythm/run?sandbox=1", "\n".join(seeds[4][1]))
rp3 = F.replay(j3.get("trace_fltnz", ""), L, allow_provisional=True) if s3 == 200 else None
res["checks"]["3_adapter_run_group1_then_python_replay"] = bool(rp3 and rp3["trace_fltnz"] == j3["trace_fltnz"] and rp3["final_sha256"] == j3["final_sha256"])
s4, j4 = call("/api/flowrhythm/verify", method="GET"); res["checks"]["3_adapter_ledger_chain_valid"] = s4 == 200 and j4.get("ok") is True
res["ledger"] = j4
res["result"] = "PASS" if all(res["checks"].values()) else "FAIL"
res["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
out = os.path.join(HERE, "MRL_selftest_receipt.json")
if os.path.exists(out):
    out = os.path.join(HERE, f"MRL_selftest_receipt_{time.strftime('%Y%m%d-%H%M%S')}.json")
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res["checks"], ensure_ascii=False, indent=1)); print(res["result"], out)
