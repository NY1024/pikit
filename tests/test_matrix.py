"""Tests for the matrix runner and experiment config."""

import json
import os
import tempfile

from pikit.config import ExperimentConfig
from pikit.matrix import MatrixRunner, ExperimentResult, save_json, save_csv, run


def test_config_defaults():
    cfg = ExperimentConfig()
    assert cfg.attacks == ["naive"]
    assert cfg.defenses == ["none"]
    assert cfg.target_spec == "mock"
    assert cfg.judge_type == "rule"


def test_config_from_dict():
    cfg = ExperimentConfig.from_dict({
        "matrix": {"attacks": ["naive", "context_ignoring"]},
        "judge": {"marker": "PWNED"},
        "target": {"spec": "mock"},
    })
    assert cfg.attacks == ["naive", "context_ignoring"]
    assert cfg.marker == "PWNED"
    assert cfg.target_spec == "mock"


def test_config_num_combinations():
    cfg = ExperimentConfig(
        attacks=["a", "b"],
        defenses=["none", "spotlighting"],
        agents=["chat"],
        channels=[""],
    )
    assert cfg.num_combinations() == 4


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


def test_matrix_verbose():
    cfg = ExperimentConfig(target_spec="mock")
    runner = MatrixRunner(cfg, verbose=True)
    # Should not raise even with verbose output to stderr.
    results = runner.run()
    assert len(results) >= 1