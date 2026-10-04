"""
MRL 神經圖建構引擎 v0.1（純 stdlib）
origin_signature: MrLiouWord ｜ 2026-10-04 ｜ Additive-Only

節點類：Repository / Branch / Commit / Role
邊類　：CONTAINS / DEFAULT_OF / SHARES_HEAD / INFERRED_AS / MIRROR_OF

輸入：
  branch_registry.json（P1 輸出；扁平 branch list）
  head_sha_duplicates.json（P1 輸出；跨命名共用 HEAD 的分組）

輸出：MRL_Branch_NeuralGraph.json、MRL_Branch_NeuralGraph.graphml
"""
from __future__ import annotations
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from role_infer import classify_registry  # noqa: E402


def build_graph(branch_registry_path: str, head_dupe_path: str = "") -> Dict:
    entries = json.load(open(branch_registry_path, encoding="utf-8"))
    sha_groups: Dict[str, List[Dict]] = {}
    if head_dupe_path and os.path.exists(head_dupe_path):
        d = json.load(open(head_dupe_path, encoding="utf-8"))
        for g in d.get("top_50", d.get("groups", [])):
            sha_groups[g["head_sha"]] = g["members"]

    classified = classify_registry(entries, sha_groups)

    nodes: List[Dict] = []
    edges: List[Dict] = []
    seen = set()

    def add_node(nid, kind, **attrs):
        if nid in seen:
            return
        seen.add(nid)
        nodes.append({"id": nid, "kind": kind, **attrs})

    def add_edge(src, dst, kind, **attrs):
        edges.append({"source": src, "target": dst, "kind": kind, **attrs})

    repos_seen: Dict[str, Dict] = {}

    for b in classified:
        full = b["full_name"]
        bid = b["branch_id"]
        role = b["inferred"]["role"]

        add_node(f"repo:{full}", "Repository",
                 owner=b["owner"], repo=b["repo"],
                 fork=b.get("repo_fork"), archived=b.get("repo_archived"),
                 default_branch=b.get("repo_default_branch"),
                 size_kb=b.get("repo_size_kb"), language=b.get("repo_language"),
                 pushed_at=b.get("repo_pushed_at"))
        repos_seen[full] = b

        add_node(f"branch:{bid}", "Branch",
                 full_name=full, name=b["branch_name"],
                 head_sha=b.get("head_sha"), protected=b.get("protected"),
                 role=role, role_confidence=b["inferred"]["confidence"])

        add_edge(f"repo:{full}", f"branch:{bid}", "CONTAINS")
        if b.get("is_default"):
            add_edge(f"repo:{full}", f"branch:{bid}", "DEFAULT_OF")

        # Role node
        rid = f"role:{role}"
        add_node(rid, "Role", role=role)
        add_edge(f"branch:{bid}", rid, "INFERRED_AS",
                 confidence=b["inferred"]["confidence"])

        # Commit node (just the sha)
        sha = b.get("head_sha")
        if sha:
            add_node(f"commit:{sha}", "Commit", sha=sha)
            add_edge(f"branch:{bid}", f"commit:{sha}", "HEAD_IS")

    # SHARES_HEAD edges (within and across repos)
    sha_to_branches: Dict[str, List[Dict]] = defaultdict(list)
    for b in classified:
        if b.get("head_sha"):
            sha_to_branches[b["head_sha"]].append(b)
    for sha, group in sha_to_branches.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b2 = group[i], group[j]
                cross_repo = a["full_name"] != b2["full_name"]
                add_edge(f"branch:{a['branch_id']}", f"branch:{b2['branch_id']}",
                         "SHARES_HEAD", head_sha=sha, cross_repo=cross_repo)
                # one of them is the canonical, the other is MIRROR_OF （confidence 低時仍標）
                # 選排序較前者（default > protected > name < other）為 canonical
                def key(x): return (not x.get("is_default"), not x.get("protected"), x["branch_name"])
                canon, mirror = (a, b2) if key(a) < key(b2) else (b2, a)
                add_edge(f"branch:{mirror['branch_id']}", f"branch:{canon['branch_id']}",
                         "MIRROR_OF", head_sha=sha)

    stats = {
        "nodes": len(nodes),
        "edges": len(edges),
        "repositories": sum(1 for n in nodes if n["kind"] == "Repository"),
        "branches": sum(1 for n in nodes if n["kind"] == "Branch"),
        "commits": sum(1 for n in nodes if n["kind"] == "Commit"),
        "shares_head_groups": sum(1 for g in sha_to_branches.values() if len(g) >= 2),
        "role_counts": {},
    }
    for b in classified:
        r = b["inferred"]["role"]
        stats["role_counts"][r] = stats["role_counts"].get(r, 0) + 1

    return {"origin_signature": "MrLiouWord",
            "generated_at": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "law": "Node + Map + Trace + Coupling 才可見；本圖僅覆蓋 Node + 部分 Map（HEAD 共用）",
            "stats": stats,
            "nodes": nodes, "edges": edges}


def to_graphml(graph: Dict) -> str:
    """最小 GraphML 輸出（Gephi / Cytoscape 可讀）。"""
    attr_defs = ['<key id="kind" for="node" attr.name="kind" attr.type="string"/>',
                 '<key id="role" for="node" attr.name="role" attr.type="string"/>',
                 '<key id="name" for="node" attr.name="name" attr.type="string"/>',
                 '<key id="full_name" for="node" attr.name="full_name" attr.type="string"/>',
                 '<key id="ekind" for="edge" attr.name="kind" attr.type="string"/>']
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">']
    out.extend(attr_defs)
    out.append('<graph edgedefault="directed">')
    for n in graph["nodes"]:
        out.append(f'<node id="{_xml(n["id"])}">')
        out.append(f'<data key="kind">{_xml(n.get("kind",""))}</data>')
        if n.get("role"): out.append(f'<data key="role">{_xml(n["role"])}</data>')
        if n.get("name"): out.append(f'<data key="name">{_xml(n["name"])}</data>')
        if n.get("full_name"): out.append(f'<data key="full_name">{_xml(n["full_name"])}</data>')
        out.append('</node>')
    for i, e in enumerate(graph["edges"]):
        out.append(f'<edge id="e{i}" source="{_xml(e["source"])}" target="{_xml(e["target"])}">')
        out.append(f'<data key="ekind">{_xml(e["kind"])}</data>')
        out.append('</edge>')
    out.append('</graph></graphml>')
    return "\n".join(out)


def _xml(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--dupes", default="")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-graphml", default="")
    args = ap.parse_args()
    g = build_graph(args.registry, args.dupes)
    json.dump(g, open(args.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if args.out_graphml:
        open(args.out_graphml, "w", encoding="utf-8").write(to_graphml(g))
    print(json.dumps(g["stats"], ensure_ascii=False, indent=1))
