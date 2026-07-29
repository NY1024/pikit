"""Tests for the matrix runner and experiment config."""

import json
import os
import tempfile

from pikit.config import ExperimentConfig
from pikit.matrix import MatrixRunner, ExperimentResult, save_json, save_jsonl, save_csv, run


def test_config_defaults():
    cfg = ExperimentConfig()
    assert cfg.attacks == ["naive"]
    assert cfg.defenses == ["none"]
    assert cfg.target_spec == "mock"
    assert cfg.judge_type == "rule"


def test_config_from_dict():
    cfg = ExperimentConfig.from_dict({
        "matrix": {"attacks": ["naive", "context_ignoring"]},
        "judge": {"canary": "PWNED"},
        "target": {"spec": "mock"},
    })
    assert cfg.attacks == ["naive", "context_ignoring"]
    assert cfg.canary == "PWNED"
    assert cfg.target_spec == "mock"


def test_config_from_toml(tmp_path):
    config_path = tmp_path / "experiment.toml"
    config_path.write_text(
        '[matrix]\nattacks = "naive"\nchannels = ""\n\n'
        '[target]\nspec = "mock"\n',
        encoding="utf-8",
    )
    cfg = ExperimentConfig.from_toml(str(config_path))
    assert cfg.attacks == ["naive"]
    assert cfg.channels == [""]
    assert cfg.target_spec == "mock"


def test_config_preserves_non_secret_target_options():
    cfg = ExperimentConfig.from_dict({
        "target": {
            "spec": "openai:deepseek-v4-flash",
            "base_url": "https://api.deepseek.com",
        },
    })
    assert cfg.target_options == {"base_url": "https://api.deepseek.com"}


def test_config_num_combinations():
    cfg = ExperimentConfig(
        attacks=["a", "b"],
        defenses=["none", "spotlighting"],
        agents=["chat"],
        channels=[""],
    )
    assert cfg.num_combinations() == 4


def test_config_num_combinations_skips_unsupported_chat_channels():
    cfg = ExperimentConfig(
        attacks=["naive"],
        defenses=["none"],
        agents=["chat", "browser"],
        channels=["", "webpage"],
    )
    # chat × direct + browser × (default + explicit webpage)
    assert cfg.num_combinations() == 3


def test_matrix_run_basic():
    """Run a minimal matrix with mock target."""
    cfg = ExperimentConfig(
        attacks=["naive"],
        defenses=["none"],
        agents=["chat"],
        channels=[""],
        target_spec="mock",
        judge_type="rule",
    )
    results = run(cfg)
    assert len(results) == 1
    r = results[0]
    assert isinstance(r, ExperimentResult)
    assert r.attack == "naive"
    assert r.agent == "chat"


def test_matrix_run_multiple():
    cfg = ExperimentConfig(
        attacks=["naive", "context_ignoring"],
        defenses=["none", "sandwich"],
        agents=["chat"],
        channels=[""],
        target_spec="mock",
    )
    results = run(cfg)
    assert len(results) == 4


def test_matrix_non_chat_empty_channel_uses_default_indirect_delivery():
    cfg = ExperimentConfig(
        attacks=["naive"],
        defenses=["none"],
        agents=["browser"],
        channels=[""],
        target_spec="mock",
        judge_type="none",
    )
    result = run(cfg)[0]
    assert result.channel == "webpage"
    assert "error:" not in result.reason


def test_matrix_save_json():
    cfg = ExperimentConfig(target_spec="mock")
    results = run(cfg)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        tmp_path = f.name
    try:
        save_json(results, tmp_path)
        with open(tmp_path) as f:
            data = json.load(f)
        assert len(data) == len(results)
        assert "attack" in data[0]
        assert "success" in data[0]
    finally:
        os.unlink(tmp_path)


def test_matrix_save_csv():
    cfg = ExperimentConfig(target_spec="mock")
    results = run(cfg)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        tmp_path = f.name
    try:
        save_csv(results, tmp_path)
        with open(tmp_path) as f:
            content = f.read()
        assert "attack" in content  # header
        assert "naive" in content   # data
    finally:
        os.unlink(tmp_path)


def test_matrix_save_jsonl_contains_structured_trace_and_metadata(tmp_path):
    results = run(ExperimentConfig(target_spec="mock"))
    output = tmp_path / "results.jsonl"
    save_jsonl(results, str(output))

    rows = [json.loads(line) for line in output.read_text().splitlines()]
    assert len(rows) == len(results)
    assert rows[0]["run_id"].startswith("run-")
    assert rows[0]["trace_data"]["schema_version"] == "pikit.trace.v1"
    assert rows[0]["metadata"]["schema_version"] == "pikit.experiment-result.v1"
    assert "attack" in rows[0]["method_specs"]


def test_matrix_result_records_rule_judge_evidence():
    result = run(ExperimentConfig(target_spec="mock"))[0]
    assert any(item["type"] == "canary" for item in result.evidence)


def test_matrix_verbose():
    cfg = ExperimentConfig(target_spec="mock")
    runner = MatrixRunner(cfg, verbose=True)
    # Should not raise even with verbose output to stderr.
    results = runner.run()
    assert len(results) >= 1
