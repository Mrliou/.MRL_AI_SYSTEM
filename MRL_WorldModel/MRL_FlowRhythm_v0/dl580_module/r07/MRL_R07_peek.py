import io,sys,json,urllib.request
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
B=r"D:\mrl\workspace\MRL_Module_Integration_20261001_R06"
tok=open(B+r"\private\modules.token",encoding="utf-8").read().strip()
req=urllib.request.Request("http://127.0.0.1:7825/api/mrl-modules/timeline"); req.add_header("Authorization","Bearer "+tok)
items=json.loads(urllib.request.urlopen(req,timeout=30).read().decode())["items"]
out=[]
for it in items:
    if not it["request_key"].startswith("R07_"): continue
    ev=json.loads(it["canonical_event"]); o=ev.get("output") or {}
    row={"seq":it["sequence"],"module":it["module_id"],"status":ev["status"],"error":ev.get("error"),"ms":ev["duration_ms"],"event_hash":it["event_hash"][:16]}
    if it["module_id"]=="flowrhythm": row.update(mode=o.get("mode"),ok=o.get("ok"),semantic=o.get("semantic_status"),final=(o.get("final_sha256") or "")[:16],byte_identical=o.get("byte_identical"))
    if it["module_id"]=="toolbox": row.update(steps=[(x["module"],((x.get("result") or {}).get("final_sha256") or (x.get("result") or {}).get("similarity") or "")) for x in o.get("results",[])])
    if it["module_id"]=="seed": row.update(model=o.get("model"),engine=(o.get("result") or {}).get("engine"),response=(o.get("result") or {}).get("response"))
    out.append(row)
json.dump(out,open(B+r"\MRL_R07_test_receipt.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False,indent=1))
