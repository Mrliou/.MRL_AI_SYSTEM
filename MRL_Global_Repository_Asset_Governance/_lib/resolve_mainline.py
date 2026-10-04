"""
P3 · 主線／分線判定（stdlib）
origin_signature: MrLiouWord ｜ 2026-10-04 ｜ Additive-Only

輸入：branch_registry.json + head_sha_duplicates.json
輸出：
  mainline_registry.json         每個 repo 一條 ACTIVE_MAINLINE（= default），列出 SUB_MAINLINE 候選
  branch_role_map.json           branch_id → role（含 confidence）扁平表
  archive_candidate_report.json  MIRROR 且與其他分支共用 HEAD、可封存的候選（**不等於可刪**）
  unmerged_asset_report.json     非 default、非 MIRROR、非 ARCHIVE 的分支（可能保有獨有資產，待 P1b/P2 驗證）
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


def resolve(reg_path: str, dupe_path: str, out_dir: str) -> Dict:
    entries = json.load(open(reg_path, encoding="utf-8"))
    groups: Dict[str, List[Dict]] = {}
    if os.path.exists(dupe_path):
        d = json.load(open(dupe_path, encoding="utf-8"))
        for g in d.get("top_50", d.get("groups", [])):
            groups[g["head_sha"]] = g["members"]
    classified = classify_registry(entries, groups)

    by_repo: Dict[str, List[Dict]] = defaultdict(list)
    for b in classified:
        by_repo[b["full_name"]].append(b)

    mainline_registry = []
    branch_role_map = {}
    archive_candidates = []
    unmerged = []

    # share-head 快取：branch_id → canonical branch_id（本 repo 內）
    canonical_of: Dict[str, str] = {}
    for sha, grp in groups.items():
        same_full = defaultdict(list)
        for m in grp:
            same_full[m["full_name"]].append(m)
        for full, members in same_full.items():
            if len(members) < 2:
                continue
            # 以 is_default > 名字短 > 字典序小 為 canonical
            members_sorted = sorted(members, key=lambda m: (not m.get("is_default"), len(m["branch_name"]), m["branch_name"]))
            canon = members_sorted[0]
            for other in members_sorted[1:]:
                canonical_of[f"{other['owner']}/{other['repo']}@{other['branch_name']}"] = f"{canon['owner']}/{canon['repo']}@{canon['branch_name']}"

    for full, branches in by_repo.items():
        default = next((b for b in branches if b.get("is_default")), None)
        if default is None:
            continue
        subs = [b for b in branches if b["inferred"]["role"] == "SUB_MAINLINE" and not b.get("is_default")]
        mainline_registry.append({
            "repository": full,
            "active_mainline": default["branch_name"],
            "active_mainline_head_sha": default.get("head_sha"),
            "sub_mainlines": [{"name": s["branch_name"], "head_sha": s.get("head_sha"),
                               "confidence": s["inferred"]["confidence"]} for s in subs],
            "total_branches": len(branches),
            "role_counts": _role_counts(branches),
        })

        for b in branches:
            bid = b["branch_id"]
            inf = b["inferred"]
            key = f"{b['owner']}/{b['repo']}@{b['branch_name']}"
            branch_role_map[bid] = {
                "full_name": full, "branch_name": b["branch_name"],
                "role": inf["role"], "confidence": inf["confidence"],
                "is_default": b.get("is_default"), "head_sha": b.get("head_sha"),
                "canonical_of": canonical_of.get(key),
            }

            if inf["role"] == "MIRROR_BRANCH" and canonical_of.get(key):
                archive_candidates.append({
                    "branch_id": bid, "full_name": full, "branch_name": b["branch_name"],
                    "head_sha": b.get("head_sha"), "canonical": canonical_of[key],
                    "confidence": inf["confidence"],
                    "reason": "shares HEAD with another branch; safe to archive (NOT delete)",
                })

            if (not b.get("is_default")
                    and inf["role"] not in ("MIRROR_BRANCH", "ARCHIVE_BRANCH")):
                unmerged.append({
                    "branch_id": bid, "full_name": full, "branch_name": b["branch_name"],
                    "role": inf["role"], "confidence": inf["confidence"],
                    "head_sha": b.get("head_sha"),
                    "note": "non-default & not mirror/archive — may hold unique assets; verify in P1b/P2 before archiving",
                })

    os.makedirs(out_dir, exist_ok=True)
    _write(out_dir, "mainline_registry.json", mainline_registry)
    _write(out_dir, "branch_role_map.json", branch_role_map)
    _write(out_dir, "archive_candidate_report.json",
           {"total": len(archive_candidates), "note": "封存候選 ≠ 允許刪除", "items": archive_candidates})
    _write(out_dir, "unmerged_asset_report.json",
           {"total": len(unmerged), "note": "P1b/P2 之前不得封存", "items": unmerged})

    return {
        "repos_resolved": len(mainline_registry),
        "branches_classified": len(classified),
        "archive_candidates": len(archive_candidates),
        "unmerged_assets": len(unmerged),
    }


def _role_counts(branches: List[Dict]) -> Dict[str, int]:
    c: Dict[str, int] = {}
    for b in branches:
        r = b["inferred"]["role"]
        c[r] = c.get(r, 0) + 1
    return c


def _write(d: str, name: str, obj):
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--dupes", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    print(json.dumps(resolve(args.registry, args.dupes, args.out_dir), ensure_ascii=False, indent=1))
