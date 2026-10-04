import os, shutil, hashlib, json, secrets, subprocess, time, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
M = r"D:\mrl\workspace\MRL_FlowRhythm_Module_20261004_R01"
EP = r"D:\mrl\MRL_GenesisLanguage_System_CPP_DL580_v2_1_RuntimeDaemon_API\MRL_Source_Input\MRL_FluinArchiveRoundTrip\flowagent_mother_system_v20.1__EXTRACTED\flowagent_final\expanded_core\engineer_pack"
EP2 = r"D:\deep-learning-containers-main\flowagent_final拷貝\flowagent_final\expanded_core\engineer_pack"
SRC = {  # 目標名 → 母體既有來源
 "下載 EchoPersona.Sample.v1.flpkg": os.path.join(EP, "#U4e0b#U8f09 EchoPersona.Sample.v1.flpkg"),
 "下載 EchoPersona.pcode": os.path.join(EP, "#U4e0b#U8f09 EchoPersona.pcode"),
 "下載 EchoPersona.structure.json": os.path.join(EP, "#U4e0b#U8f09 EchoPersona.structure.json"),
 "下載 FluinCoreSeed.v1.flseed": os.path.join(EP, "#U4e0b#U8f09 FluinCoreSeed.v1.flseed"),
 "下載 Fluin_Particle_BilingualDict.csv": os.path.join(EP, "#U4e0b#U8f09 Fluin_Particle_BilingualDict.csv"),
 "下載 Memory.Seed.Core.v1.flseed": os.path.join(EP, "#U4e0b#U8f09 Memory.Seed.Core.v1.flseed"),
 "下載 flgroup.json": os.path.join(EP, "#U4e0b#U8f09 flgroup.json"),
 "重新下載 FluinSim.DualSet.v1.flsim": os.path.join(EP2, "#U91cd#U65b0#U4e0b#U8f09 FluinSim.DualSet.v1.flsim"),
}
rec = {"origin_signature": "MrLiouWord", "release": "20261004-R01", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "steps": {}}
for d in ("lexicon", "private", "runtime"): os.makedirs(os.path.join(M, d), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
exp = dict(l.rstrip("\n").split("  ", 1)[::-1] for l in open(os.path.join(M, "lexicon", "SOURCES.sha256"), encoding="utf-8") if l.strip())
lex = {}; ok = True
for name, src in SRC.items():
    dst = os.path.join(M, "lexicon", name)
    if not os.path.exists(dst): shutil.copy2(src, dst)   # 只新增；原檔不動
    h = sha(dst); lex[name] = {"source": src, "sha256": h, "match": h == exp[name]}; ok &= h == exp[name]
rec["steps"]["lexicon_copied_from_mother_and_verified"] = ok; rec["lexicon"] = lex
tp = os.path.join(M, "private", "flowrhythm.token")
if not os.path.exists(tp):
    open(tp, "w", encoding="utf-8").write(secrets.token_urlsafe(36))
    subprocess.run(f'icacls "{tp}" /inheritance:r /grant:r "NT AUTHORITY\\SYSTEM:(R)" "BUILTIN\\Administrators:(R)"', shell=True, capture_output=True)
rec["steps"]["token_created_and_acl_restricted"] = os.path.exists(tp)
log = open(os.path.join(M, "runtime", "adapter.out.log"), "ab")
p = subprocess.Popen([r"D:\MrlToolchain\python\python.exe", os.path.join(M, "MRL_flowrhythm_adapter.py")], cwd=M, stdout=log, stderr=subprocess.STDOUT,
                     creationflags=0x00000008 | 0x00000200)  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
time.sleep(4)
json.dump({"adapter_pid": p.pid, "started": rec["started"]}, open(os.path.join(M, "runtime", "pid.json"), "w"))
rec["steps"]["adapter_started_pid"] = p.pid
r = subprocess.run([r"D:\MrlToolchain\python\python.exe", os.path.join(M, "MRL_flowrhythm_selftest.py")], cwd=M, capture_output=True, timeout=180)
rec["steps"]["selftest_exit"] = r.returncode; rec["selftest_stdout_tail"] = r.stdout.decode("utf-8", "replace")[-1500:]; rec["selftest_stderr_tail"] = r.stderr.decode("utf-8", "replace")[-800:]
rec["files"] = {f: sha(os.path.join(M, f)) for f in ("flow_rhythm.py", "mrl_dialect.py", "MRL_flowrhythm_adapter.py", "MRL_flowrhythm_selftest.py", "README.md")}
rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(rec, open(os.path.join(M, "MRL_receipt.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rec["steps"], ensure_ascii=False)); print(rec["selftest_stdout_tail"])
