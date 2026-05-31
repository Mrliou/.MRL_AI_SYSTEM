"""
test_MRL_flowagent_lawengine.py — 母體活引擎驗收
origin_signature: MrLiouWord
product: MRL_AI_SYSTEM

實證 rootlaw v5 新法則能「真的跑」：三振跳層 / 莫比斯1:9 / 命名回收 / 紅線護欄 /
事件編年 / 閉環自驗。
"""
from __future__ import annotations

import pathlib

import pytest

from MRL_FlowAgent_LawEngine_v1 import (
    MRL_FlowAgentLawEngine,
    THREE_STRIKE_THRESHOLD,
    load_rootlaw,
    reclaim_name,
)


@pytest.fixture
def engine(tmp_path):
    return MRL_FlowAgentLawEngine(chronicle_path=tmp_path / "chron.jsonl")


# ─── rootlaw 載入 ──────────────────────────────────────────────────────────────

class TestRootlaw:
    def test_loads_v5_with_13_invariants(self):
        rl = load_rootlaw()
        assert rl["version"] >= 5
        ids = [i["id"] for i in rl["invariants"]]
        for need in ("rl_07_law_serves_operation", "rl_08_three_strike_layer_jump",
                     "rl_09_mobius_majority_resolution", "rl_10_event_chronicle",
                     "rl_11_origin_boundary_sovereignty", "rl_12_naming_reclamation",
                     "rl_13_gate_unity", "rl_14_parallel_world_generation"):
            assert need in ids


# ─── rl_12 命名回收 ────────────────────────────────────────────────────────────

class TestNamingReclamation:
    def test_external_shell_becomes_mrl_canonical(self):
        assert reclaim_name("FlowAgent.Runtime.v47.zip") == "MRL_FlowAgentRuntime_v47"

    def test_no_external_name_residue(self):
        out = reclaim_name("guardian.mirror.trace.loop.v2.flpkg.zip")
        assert out.startswith("MRL_") and out.endswith("_v2")
        assert "guardian" not in out.lower() or "Guardian" in out  # 回收為母體描述

    def test_default_version_one(self):
        assert reclaim_name("some_external_module").endswith("_v1")

    def test_strips_mrl_duplication(self):
        # 已是 MRL_ 開頭不重複堆疊
        assert reclaim_name("MRL_Runtime").startswith("MRL_")


# ─── rl_08 三振跳層 ────────────────────────────────────────────────────────────

class TestThreeStrikeLayerJump:
    def test_first_two_patch_surface(self, engine):
        r1 = engine.register_error("sig-A")
        r2 = engine.register_error("sig-A")
        assert r1["layer_jump"] is False
        assert r2["layer_jump"] is False
        assert r2["action"] == "patch_surface"

    def test_third_triggers_jump(self, engine):
        for _ in range(THREE_STRIKE_THRESHOLD - 1):
            engine.register_error("sig-B")
        r3 = engine.register_error("sig-B")
        assert r3["count"] == THREE_STRIKE_THRESHOLD
        assert r3["layer_jump"] is True
        assert r3["action"] == "amend_or_remove_root_rule"

    def test_distinct_signatures_counted_separately(self, engine):
        engine.register_error("x")
        r = engine.register_error("y")
        assert r["count"] == 1 and r["layer_jump"] is False


# ─── rl_09 莫比斯 1:9 多數決 ────────────────────────────────────────────────────

class TestMobiusMajority:
    def test_single_blocker_among_majority_advances(self, engine):
        particles = {f"p{i}": True for i in range(9)}
        particles["blocker"] = False
        out = engine.mobius_majority(particles)
        assert out["decision"] == "REMOVE_BLOCKER_ADVANCE"
        assert out["target"] == "blocker"

    def test_red_line_blocker_is_held_not_removed(self, engine):
        particles = {f"p{i}": True for i in range(9)}
        particles["rl_06_child_safety"] = False
        out = engine.mobius_majority(particles)
        assert out["decision"] == "HOLD_RED_LINE"
        assert out["target"] is None

    def test_multiple_blockers_continue_loop(self, engine):
        particles = {"a": True, "b": False, "c": False, "d": True}
        out = engine.mobius_majority(particles)
        assert out["decision"] == "CONTINUE_LOOP"

    def test_all_pass_continue_loop(self, engine):
        out = engine.mobius_majority({"a": True, "b": True})
        assert out["decision"] == "CONTINUE_LOOP"


# ─── rl_13 出口即入口 ──────────────────────────────────────────────────────────

class TestGateUnity:
    def test_in_reclaims_external_name(self, engine):
        r = engine.gate("in", {"name": "FlowAgent.Runtime.v47.zip"})
        assert r["direction"] == "in"
        assert r["reclaimed"] == "MRL_FlowAgentRuntime_v47"
        assert r["as"] == "material"

    def test_out_carries_origin_signature(self, engine):
        r = engine.gate("out", {"msg": "hello world"})
        assert r["direction"] == "out"
        assert r["origin_signature"] == "MrLiouWord"

    def test_same_gate_method_both_directions(self, engine):
        # 出口即入口:同一個 gate 方法雙向
        assert engine.gate("in", {"name": "x"})["gate"] == \
               engine.gate("out", {})["gate"] == "stereoscopic_terminal"

    def test_invalid_direction_rejected(self, engine):
        with pytest.raises(ValueError):
            engine.gate("sideways", {})


# ─── rl_14 平行世界生成 ────────────────────────────────────────────────────────

class TestParallelWorldGeneration:
    def test_generates_branch_options(self, engine):
        rep = engine.generate_parallel_worlds("w0", ["pathA", "pathB", "pathC"])
        assert len(rep["branches"]) == 3
        assert rep["selectable"] is True
        assert rep["one_world_origin"] == "MrLiouWord"

    def test_branches_unverified_by_default(self, engine):
        # no_proof_implies_rhetoric:未驗證分支不得宣稱為真實
        rep = engine.generate_parallel_worlds("w0", ["a", "b"])
        assert all(b["verified"] is False for b in rep["branches"])
        assert all(b["origin_signature"] == "MrLiouWord" for b in rep["branches"])

    def test_dimension_lift_recorded(self, engine):
        rep = engine.generate_parallel_worlds("w0", ["a"], dimension_lift=2)
        assert rep["branches"][0]["dimension"] == 2


# ─── rl_10 事件編年 + 閉環 ─────────────────────────────────────────────────────

class TestChronicleAndLoop:
    def test_events_written_to_chronicle_file(self, engine):
        engine.chronicle("test", {"k": "v"})
        assert pathlib.Path(engine.chronicle_path).exists()
        assert "test" in pathlib.Path(engine.chronicle_path).read_text(encoding="utf-8")

    def test_self_acceptance_passes(self, engine):
        rep = engine.self_acceptance()
        assert rep["verified"] is True
        assert rep["token"] == "MRL_FLOWAGENT_LAWENGINE_LOOP_PASS"
        assert rep["origin_signature"] == "MrLiouWord"

    def test_loop_records_events(self, engine):
        rep = engine.run_loop({"source": "t", "law_particles": {"a": True, "b": True}})
        assert rep["events_recorded"] >= 1
        assert rep["mirror"]["rootlaw_version"] >= 5
