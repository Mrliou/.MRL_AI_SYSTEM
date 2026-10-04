import io,sys,json,urllib.request,uuid
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
B=r"D:\mrl\workspace\MRL_Module_Integration_20261001_R06"; FR=r"D:\mrl\workspace\MRL_FlowRhythm_Module_20261004_R01"
tok=open(B+r"\private\modules.token",encoding="utf-8").read().strip()
tr=open(FR+r"\runtime\dl580_group1_live.trace.fltnz",encoding="utf-8").read()
req=urllib.request.Request("http://127.0.0.1:7825/api/mrl-modules/run",data=json.dumps({"module":"flowrhythm","input":{"mode":"replay","sandbox":True,"text":tr}}).encode(),method="POST")
for k,v in {"Authorization":"Bearer "+tok,"Content-Type":"application/json","Idempotency-Key":"R07_replay_"+uuid.uuid4().hex[:12]}.items(): req.add_header(k,v)
r=json.loads(urllib.request.urlopen(req,timeout=60).read().decode())["row"]
ev=json.loads(r["canonical_event"]); o=ev["output"]
print(json.dumps({"seq":r["sequence"],"status":ev["status"],"byte_identical":o.get("byte_identical"),"final":o["final_sha256"][:16],"trace_ops":o.get("trace_ops"),"event_hash":r["event_hash"][:16]},ensure_ascii=False))
