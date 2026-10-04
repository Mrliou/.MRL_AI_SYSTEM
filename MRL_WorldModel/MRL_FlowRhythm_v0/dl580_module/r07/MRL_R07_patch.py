"""
R07 · 接通：FlowRhythm 模組 → 7825 模組管線；AI 執行服務 → 母體本機推理 7500；開機排程納管 7827
origin_signature: MrLiouWord ｜ 2026-10-04 ｜ 每個被改的檔先存 .bak-20261004-R07，錨點不符即中止、不寫入
"""
import io, json, os, shutil, subprocess, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
B = r"D:\mrl\workspace\MRL_Module_Integration_20261001_R06"
FR = r"D:\mrl\workspace\MRL_FlowRhythm_Module_20261004_R01"
TAG = ".bak-20261004-R07"
rec = {"origin_signature": "MrLiouWord", "release": "R07", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "edits": {}}

def edit(path, anchor, new, mode="insert_before"):
    t = open(path, encoding="utf-8").read()
    assert t.count(anchor) == 1, f"anchor not unique in {path}: {anchor[:60]}"
    if not os.path.exists(path + TAG): shutil.copy2(path, path + TAG)
    out = t.replace(anchor, (new + anchor) if mode == "insert_before" else new)
    open(path, "w", encoding="utf-8", newline="\n").write(out)
    rec["edits"][os.path.relpath(path, B)] = {"backup": os.path.basename(path) + TAG, "bytes_before": len(t.encode()), "bytes_after": len(out.encode())}

# A. MRL_core.mjs — 新增 flowrhythm case（插在 default 前）
core = B + r"\release\modules\MRL_core.mjs"
edit(core, "  default:throw new BankError(404,'模組不存在');",
"""  case 'flowrhythm':{ // R07 2026-10-04 接通 MRL_FlowRhythm_Module_20261004_R01（127.0.0.1:7827；本體 flow_rhythm.py）
   requireThat(typeof env.MRL_FLOWRHYTHM_URL==='string'&&env.MRL_FLOWRHYTHM_URL&&env.MRL_FLOWRHYTHM_TOKEN,'FlowRhythm 模組尚未連接');
   const mode=input.mode==='replay'?'replay':'run';requireThat(typeof input.text==='string'&&input.text.length>0&&input.text.length<=30000,'需要 text（粒子語句或軌跡）');
   const q=new URLSearchParams();if(input.sandbox)q.set('sandbox','1');if(typeof input.title==='string'&&input.title.length<=120)q.set('title',input.title);
   const r=await fetch(env.MRL_FLOWRHYTHM_URL+'/api/flowrhythm/'+mode+'?'+q,{method:'POST',headers:{Authorization:'Bearer '+env.MRL_FLOWRHYTHM_TOKEN,'Content-Type':'text/plain; charset=utf-8'},body:input.text});
   const out=await r.json();if(!r.ok)throw new BankError(r.status===422?422:502,out.error||'FlowRhythm 執行失敗');return out;}
""")

# B. MRL_local_server.mjs — AI 執行服務綁定母體本機推理；傳入 FlowRhythm 連線
srv = B + r"\release\modules\MRL_local_server.mjs"
edit(srv, "const worker=createModuleWorker(createWorker({}));",
"""// R07 2026-10-04：AI 執行服務 = 母體本機推理引擎 127.0.0.1:7500（MRL_Inference_API，Qwen2.5-32B；人格路由與記憶檢索在引擎端）
const AI=process.env.MRL_INFERENCE_KEY?{async run(model,{messages=[],max_tokens=2048}={}){const user=[...messages].reverse().find(m=>m.role==='user')?.content||'';const r=await fetch((process.env.MRL_INFERENCE_URL||'http://127.0.0.1:7500')+'/MRL_chat',{method:'POST',headers:{'Content-Type':'application/json','x-api-key':process.env.MRL_INFERENCE_KEY},body:JSON.stringify({message:user,max_tokens:Math.min(max_tokens,2048),persona:process.env.MRL_AI_PERSONA||undefined})});const out=await r.json();if(!r.ok||out.ok===false)throw new Error(out.error||'inference failed');return {response:out.response,session_id:out.session_id,model,engine:'MRL_Particle_Inference_Engine@7500'};}}:undefined;
""")
edit(srv, "{DB,MRL_BANK_SERVICE_KEY:token,OPENWEATHER_API_KEY:process.env.OPENWEATHER_API_KEY}",
     "{DB,MRL_BANK_SERVICE_KEY:token,OPENWEATHER_API_KEY:process.env.OPENWEATHER_API_KEY,AI,MRL_AI_MODEL:process.env.MRL_AI_MODEL,MRL_FLOWRHYTHM_URL:process.env.MRL_FLOWRHYTHM_URL,MRL_FLOWRHYTHM_TOKEN:process.env.MRL_FLOWRHYTHM_TOKEN}", mode="replace")

# C. MRL_start_modules.py — 環境與納管 flowrhythm 子程序（開機排程 MRL_Modules_20261001_R06 一併帶起）
st = B + r"\MRL_start_modules.py"
edit(st, "env=dict(os.environ,MRL_LOCAL_TOKEN=token,MRL_DATA_DIR=str(BASE/'runtime'),MRL_MODULE_PORT='7825',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')",
"""FR=pathlib.Path(r'D:\\mrl\\workspace\\MRL_FlowRhythm_Module_20261004_R01')  # R07 2026-10-04
env=dict(os.environ,MRL_LOCAL_TOKEN=token,MRL_DATA_DIR=str(BASE/'runtime'),MRL_MODULE_PORT='7825',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',
 MRL_FLOWRHYTHM_URL='http://127.0.0.1:7827',MRL_FLOWRHYTHM_TOKEN=(FR/'private/flowrhythm.token').read_text().strip(),
 MRL_AI_MODEL='Qwen2.5-32B-Instruct',MRL_INFERENCE_URL='http://127.0.0.1:7500',MRL_INFERENCE_KEY=(BASE/'private/inference.key').read_text().strip())""", mode="replace")
edit(st, "'flowcore':[r'D:\\MrlToolchain\\python\\python.exe',str(BASE/'release/modules/MRL_flowcore_adapter.py'),'--data-dir',str(BASE/'runtime/flowcore'),'--port','7826']}",
     "'flowcore':[r'D:\\MrlToolchain\\python\\python.exe',str(BASE/'release/modules/MRL_flowcore_adapter.py'),'--data-dir',str(BASE/'runtime/flowcore'),'--port','7826'],'flowrhythm':[r'D:\\MrlToolchain\\python\\python.exe',str(FR/'MRL_flowrhythm_adapter.py')]}", mode="replace")

# D. MRL_registry.json — 新增目錄項（append-only）
reg = B + r"\release\modules\MRL_registry.json"
items = json.load(open(reg, encoding="utf-8"))
if not any(m.get("id") == "flowrhythm" for m in items):
    if not os.path.exists(reg + TAG): shutil.copy2(reg, reg + TAG)
    items.append({"id": "flowrhythm", "title": "FlowRhythm 語場節奏（母體本機）",
                  "description": "Jump → Collapse → Trace → Replay；本體 flow_rhythm.py v0.2.0，字典為母體 2025-07 原檔；正典預設拒絕 provisional 映射，sandbox 才允許",
                  "source_files": ["MRL_FlowRhythm_Module_20261004_R01/flow_rhythm.py", "MRL_FlowRhythm_Module_20261004_R01/lexicon/SOURCES.sha256"],
                  "mode": "executable",
                  "example": {"mode": "run", "sandbox": True, "title": "EchoPersona", "text": "⊕Core: Echo.Persona\n⋄fx.adj.112\n⋄fx.noun.024\n∴\n⋄fx.flow.007\n⊗Memory.SelfReflect"}})
    json.dump(items, open(reg, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    rec["edits"]["release/modules/MRL_registry.json"] = {"backup": "MRL_registry.json" + TAG, "appended": "flowrhythm"}

# E. 推理金鑰檔（與 Bridge 同一把；只給 SYSTEM/Administrators）
kp = B + r"\private\inference.key"
if not os.path.exists(kp):
    open(kp, "w", encoding="utf-8").write("MrLiouWord2026")
    subprocess.run(f'icacls "{kp}" /inheritance:r /grant:r "NT AUTHORITY\\SYSTEM:(R)" "BUILTIN\\Administrators:(R)"', shell=True, capture_output=True)
rec["edits"]["private/inference.key"] = "created"

# F. 停掉我今天手動起的 7827（PID 見 FR\runtime\pid.json），改由排程監督程序接管；重啟排程 MRL_Modules_20261001_R06
pid = json.load(open(FR + r"\runtime\pid.json")).get("adapter_pid")
subprocess.run(f"taskkill /pid {pid} /f", shell=True, capture_output=True)
live = json.load(open(B + r"\MRL_live_pids.json"))
# 監督程序 = modules 子程序的父程序
par = subprocess.run(f'wmic process where "ProcessId={live["modules"]}" get ParentProcessId /value', shell=True, capture_output=True).stdout.decode("utf-8", "replace")
sup = int([l for l in par.splitlines() if "ParentProcessId=" in l][0].split("=")[1])
rec["supervisor_pid_before"] = sup
subprocess.run(f"taskkill /pid {sup} /t /f", shell=True, capture_output=True)
time.sleep(2)
r = subprocess.run("schtasks /run /tn MRL_Modules_20261001_R06", shell=True, capture_output=True)
rec["schtasks_run"] = r.returncode
time.sleep(12)
rec["live_pids_after"] = json.load(open(B + r"\MRL_live_pids.json"))
rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(rec, open(B + r"\MRL_R07_patch_receipt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rec, ensure_ascii=False, indent=1))
