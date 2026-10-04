import io,sys,json,urllib.request,time,uuid,zipfile,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
B=r"D:\mrl\workspace\MRL_Module_Integration_20261001_R06"; FR=r"D:\mrl\workspace\MRL_FlowRhythm_Module_20261004_R01"
tok=open(B+r"\private\modules.token",encoding="utf-8").read().strip()
def call(path,body=None,method="GET"):
    req=urllib.request.Request("http://127.0.0.1:7825/api/mrl-modules"+path,data=json.dumps(body).encode() if body is not None else None,method=method)
    req.add_header("Authorization","Bearer "+tok)
    if body is not None: req.add_header("Content-Type","application/json"); req.add_header("Idempotency-Key","R07_"+uuid.uuid4().hex[:20])
    try:
        with urllib.request.urlopen(req,timeout=120) as r: return r.status,json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return e.code,json.loads(e.read().decode() or "{}")
res={}
s,c=call("/catalog"); res["catalog"]={"status":s,"integrations":c.get("integrations"),"modules":[m["id"] for m in c.get("modules",[])]}
with zipfile.ZipFile(FR+r"\lexicon\重新下載 FluinSim.DualSet.v1.flsim") as z: g1=z.read("Group1_EchoPersona.fltnz").decode("utf-8")
s,r=call("/run",{"module":"flowrhythm","input":{"mode":"run","sandbox":True,"title":"R07_Group1","text":g1}},"POST")
out=r.get("row",{}).get("output") or {}
res["flowrhythm_run"]={"status":s,"ok":out.get("ok"),"final_sha256":(out.get("final_sha256") or "")[:16],"semantic_status":out.get("semantic_status"),"event_hash":(r.get("row",{}).get("event_hash") or "")[:16],"error":r.get("row",{}).get("error") or r.get("error")}
tr=out.get("trace_fltnz","")
s,r2=call("/run",{"module":"flowrhythm","input":{"mode":"replay","sandbox":True,"text":tr}},"POST")
o2=r2.get("row",{}).get("output") or {}
res["flowrhythm_replay"]={"status":s,"byte_identical":o2.get("byte_identical"),"final_sha256":(o2.get("final_sha256") or "")[:16],"error":r2.get("row",{}).get("error") or r2.get("error")}
s,r3=call("/run",{"module":"flowrhythm","input":{"mode":"run","text":g1}},"POST")  # 正典 → 422 預期
res["flowrhythm_canonical"]={"status":s,"error":r3.get("row",{}).get("error") or r3.get("error")}
s,r4=call("/run",{"module":"toolbox","input":{"steps":[{"module":"flowrhythm","input":{"mode":"run","sandbox":True,"title":"R07_pipeline","text":g1}},{"module":"simhash","input":{"text1":"怎麼過去就怎麼回來","text2":"怎麼過去就怎麼回來"}}]}},"POST")
o4=r4.get("row",{}).get("output") or {}
res["toolbox_pipeline"]={"status":s,"steps":[x.get("module") for x in o4.get("results",[])],"first_final":((o4.get("results") or [{}])[0].get("result") or {}).get("final_sha256","")[:16],"error":r4.get("row",{}).get("error") or r4.get("error")}
t0=time.time(); s,r5=call("/run",{"module":"seed","input":{"prompt":"用一句話說明「怎麼過去，就怎麼回來」在 MRL 語場裡的意思。"}},"POST")
o5=r5.get("row",{}).get("output") or {}
res["seed_local_ai"]={"status":s,"model":o5.get("model"),"provider_connected":o5.get("provider_connected"),"engine":(o5.get("result") or {}).get("engine"),"response":((o5.get("result") or {}).get("response") or "")[:300],"seconds":round(time.time()-t0,1),"error":r5.get("row",{}).get("error") or r5.get("error")}
s,v=call("/verify"); res["ledger_verify"]=v
json.dump(res,open(B+r"\MRL_R07_test_receipt.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
