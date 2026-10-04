"""
MRL 分支角色推斷引擎（純 stdlib；規則見 branch_role_rules.yaml）
origin_signature: MrLiouWord ｜ 2026-10-04 ｜ Additive-Only
"""
from __future__ import annotations
import os
import re
from typing import Dict, List, Optional, Tuple

ROLES = (
    "ROOT_MAINLINE", "ACTIVE_MAINLINE", "SUB_MAINLINE", "FEATURE_BRANCH",
    "RECOVERY_BRANCH", "MIRROR_BRANCH", "EXTERNAL_SOURCE_BRANCH",
    "ARCHIVE_BRANCH", "ORPHAN_BRANCH", "UNKNOWN_BRANCH",
)

# 內嵌 fallback 規則（與 branch_role_rules.yaml 同步；避免需裝 PyYAML）
_PREFIX_RULES: Dict[str, Dict] = {
    "main":          {"role": "ROOT_MAINLINE",          "confidence": 0.95, "note": "典型 git root"},
    "master":        {"role": "ROOT_MAINLINE",          "confidence": 0.95, "note": "典型 git root"},
    "develop":       {"role": "ACTIVE_MAINLINE",        "confidence": 0.80, "note": "常見開發主線"},
    "copilot":       {"role": "MIRROR_BRANCH",          "confidence": 0.95, "note": "GitHub Copilot 自動生成前綴"},
    "claude":        {"role": "MIRROR_BRANCH",          "confidence": 0.95, "note": "Claude agent 自動生成前綴"},
    "codex":         {"role": "MIRROR_BRANCH",          "confidence": 0.90, "note": "Codex agent 自動生成前綴"},
    "agent":         {"role": "MIRROR_BRANCH",          "confidence": 0.85, "note": "通用 agent 前綴"},
    "MRL_recovered": {"role": "RECOVERY_BRANCH",        "confidence": 0.95, "note": "MR.Liou recover 前綴"},
    "recovered":     {"role": "RECOVERY_BRANCH",        "confidence": 0.90, "note": "recover 前綴"},
    "recover":       {"role": "RECOVERY_BRANCH",        "confidence": 0.90, "note": "recover 前綴"},
    "evidence":      {"role": "ARCHIVE_BRANCH",         "confidence": 0.90, "note": "證據封存前綴"},
    "archive":       {"role": "ARCHIVE_BRANCH",         "confidence": 0.95, "note": "封存前綴"},
    "archived":      {"role": "ARCHIVE_BRANCH",         "confidence": 0.95, "note": "封存前綴"},
    "backup":        {"role": "ARCHIVE_BRANCH",         "confidence": 0.95, "note": "備份前綴"},
    "external":      {"role": "EXTERNAL_SOURCE_BRANCH", "confidence": 0.90, "note": "外部來源"},
    "vendor":        {"role": "EXTERNAL_SOURCE_BRANCH", "confidence": 0.85, "note": "外部 vendor"},
    "upstream":      {"role": "EXTERNAL_SOURCE_BRANCH", "confidence": 0.85, "note": "upstream 鏡像"},
    "mirror":        {"role": "EXTERNAL_SOURCE_BRANCH", "confidence": 0.80, "note": "鏡像"},
    "feature":       {"role": "FEATURE_BRANCH",         "confidence": 0.80, "note": "功能分支"},
    "feat":          {"role": "FEATURE_BRANCH",         "confidence": 0.80, "note": "功能分支"},
    "fix":           {"role": "FEATURE_BRANCH",         "confidence": 0.80, "note": "修復分支"},
    "hotfix":        {"role": "FEATURE_BRANCH",         "confidence": 0.80, "note": "熱修復分支"},
    "release":       {"role": "SUB_MAINLINE",           "confidence": 0.70, "note": "release 線"},
    "worldmodel":    {"role": "SUB_MAINLINE",           "confidence": 0.75, "note": "世界模型次主線"},
    "MRL_AI_SYSTEM": {"role": "SUB_MAINLINE",           "confidence": 0.80, "note": "MRL_AI_SYSTEM 路徑型次主線"},
}

_SUBSTRING_HINTS: List[Dict] = [
    {"contains": "wip",  "role": "FEATURE_BRANCH", "confidence": 0.55},
    {"contains": "test", "role": "FEATURE_BRANCH", "confidence": 0.55},
]


def _first_segment(name: str) -> Tuple[str, bool]:
    """回傳 (第一段, has_slash)。name 可能是 'copilot/foo/bar' → ('copilot', True)。"""
    if "/" in name:
        return name.split("/", 1)[0], True
    return name, False


def infer_role(
    branch_name: str,
    *,
    is_default: bool = False,
    protected: bool = False,
    ahead: Optional[int] = None,
    behind: Optional[int] = None,
    unique_commits: Optional[int] = None,
    shares_head_with_other: Optional[bool] = None,
) -> Dict:
    """
    回傳：{
      "role": <ROLE>, "confidence": float, "evidence": [str, ...],
      "candidates": [(role, confidence, note), ...]  # 排序：confidence desc
    }
    """
    candidates: List[Tuple[str, float, str]] = []
    seg, has_slash = _first_segment(branch_name)

    # 1) prefix 命中（含 default branch 也可能是 'main' / 'master' 型）
    if seg in _PREFIX_RULES:
        r = _PREFIX_RULES[seg]
        candidates.append((r["role"], r["confidence"], f"prefix='{seg}': {r['note']}"))

    # 2) default branch 的 floor（+0 confidence，當作下限）
    if is_default:
        candidates.append(("ACTIVE_MAINLINE", 0.85, "is_default=True → 至少是 ACTIVE_MAINLINE"))

    # 3) 名稱子字串線索
    low = branch_name.lower()
    for h in _SUBSTRING_HINTS:
        if h["contains"] in low:
            candidates.append((h["role"], h["confidence"], f"name contains '{h['contains']}'"))

    # 4) 內容線索（有量才用）
    if shares_head_with_other is True:
        candidates.append(("MIRROR_BRANCH", 0.90, "shares HEAD sha with another branch (dedupe)"))
    if unique_commits is not None and unique_commits == 0:
        candidates.append(("MIRROR_BRANCH", 0.90, "unique_commits==0"))
    if ahead is not None and behind is not None and ahead == 0 and behind > 100:
        candidates.append(("ARCHIVE_BRANCH", 0.75, f"ahead=0 & behind={behind}>100 → 停滯"))

    # 5) 選 confidence 最高者；若無任何證據 → UNKNOWN
    if not candidates:
        role = "UNKNOWN_BRANCH"
        conf = 0.20
        why = ["無任何前綴／內容證據；保守為 UNKNOWN"]
    else:
        candidates.sort(key=lambda x: x[1], reverse=True)
        role, conf, note = candidates[0]
        why = [note]
        # ROOT_MAINLINE 優先於 ACTIVE_MAINLINE：若 default + ROOT 前綴，升為 ROOT
        if is_default and any(c[0] == "ROOT_MAINLINE" for c in candidates):
            role = "ROOT_MAINLINE"
            conf = max(conf, 0.95)
            why.append("is_default=True 且命中 ROOT 前綴 → 升為 ROOT_MAINLINE")

    return {
        "role": role,
        "confidence": round(conf, 3),
        "evidence": why,
        "candidates": [{"role": r, "confidence": round(c, 3), "note": n} for r, c, n in candidates],
    }


def classify_registry(entries: List[Dict], head_sha_groups: Optional[Dict[str, List]] = None) -> List[Dict]:
    """對 branch_registry.json 的 entries 批次分類。head_sha_groups 可選，用來標 shares_head_with_other。"""
    shares: Dict[str, bool] = {}
    if head_sha_groups:
        for sha, members in head_sha_groups.items():
            if len(members) >= 2:
                for m in members:
                    key = f"{m['owner']}/{m['repo']}@{m['branch_name']}"
                    shares[key] = True
    out = []
    for e in entries:
        key = f"{e['owner']}/{e['repo']}@{e['branch_name']}"
        result = infer_role(
            e["branch_name"],
            is_default=bool(e.get("is_default")),
            protected=bool(e.get("protected")),
            shares_head_with_other=shares.get(key, None),
        )
        out.append({**e, **{"inferred": result}})
    return out
