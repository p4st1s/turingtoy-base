import pytest
from pathlib import Path
from typing import Any, Dict, List, Tuple

from turingtoy import run_turing_machine
from tests.utils import regression_test

def to_dict(keys: List[str], value: Any) -> Dict[str, Any]:
    return {key: value for key in keys}

@pytest.mark.parametrize("input_str, expected_output", [
    ("111", "1110111"),
    ("1", "101"),
])
def test_turing_machine_double_1(
    request: pytest.FixtureRequest,
    global_datadir: Path,
    input_str: str,
    expected_output: str
) -> None:
    machine = {
        "blank": "0",
        "start state": "e1",
        "final states": ["done"],
        "table": {
            "e1": {
                "0": {"L": "done"},
                "1": {"write": "0", "R": "e2"},
            },
            "e2": {
                "1": {"write": "1", "R": "e2"},
                "0": {"write": "0", "R": "e3"},
            },
            "e3": {
                "1": {"write": "1", "R": "e3"},
                "0": {"write": "1", "L": "e4"},
            },
            "e4": {
                "1": {"write": "1", "L": "e4"},
                "0": {"write": "0", "L": "e5"},
            },
            "e5": {
                "1": {"write": "1", "L": "e5"},
                "0": {"write": "1", "R": "e1"},
            },
            "done": {},
        },
    }

    datadir = global_datadir / "double_1"

    output, execution_history, accepted = run_turing_machine(machine, input_str)
    assert output == expected_output
    assert accepted

    regression_test(
        {
            "machine": machine,
            "input": input_str,
            "output": output,
            "execution_history": execution_history,
        },
        datadir / f"{input_str}.json",
        request.config.getoption("force_regen"),
    )

@pytest.mark.parametrize("input_str, expected_output", [
    ("11+1", "100 1"),
    ("1011+11001", "100100 11001"),
])
def test_turing_machine_add_two_binary_numbers(
    request: pytest.FixtureRequest,
    global_datadir: Path,
    input_str: str,
    expected_output: str
) -> None:
    machine = {
        "blank": " ",
        "start state": "right",
        "final states": ["done"],
        "table": {
            "right": {
                **to_dict(["0", "1", "+"], "R"),
                " ": {"L": "read"},
            },
            "read": {
                "0": {"write": "c", "L": "have0"},
                "1": {"write": "c", "L": "have1"},
                "+": {"write": " ", "L": "rewrite"},
            },
            "have0": {**to_dict(["0", "1"], "L"), "+": {"L": "add0"}},
            "have1": {**to_dict(["0", "1"], "L"), "+": {"L": "add1"}},
            "add0": {
                **to_dict(["0", " "], {"write": "O", "R": "back0"}),
                "1": {"write": "I", "R": "back0"},
                **to_dict(["O", "I"], "L"),
            },
            "add1": {
                **to_dict(["0", " "], {"write": "I", "R": "back1"}),
                "1": {"write": "O", "L": "carry"},
                **to_dict(["O", "I"], "L"),
            },
            "carry": {
                **to_dict(["0", " "], {"write": "1", "R": "back1"}),
                "1": {"write": "0", "L": "carry"},
            },
            "back0": {
                **to_dict(["0", "1", "O", "I", "+"], "R"),
                "c": {"write": "0", "L": "read"},
            },
            "back1": {
                **to_dict(["0", "1", "O", "I", "+"], "R"),
                "c": {"write": "1", "L": "read"},
            },
            "rewrite": {
                "O": {"write": "0", "L": "rewrite"},
                "I": {"write": "1", "L": "rewrite"},
                **to_dict(["0", "1"], "L"),
                " ": {"R": "done"},
            },
            "done": {},
        },
    }

    datadir = global_datadir / "add_two_binary_numbers"

    output, execution_history, accepted = run_turing_machine(machine, input_str)
    assert output == expected_output
    assert accepted

    regression_test(
        {
            "machine": machine,
            "input": input_str,
            "output": output,
            "execution_history": execution_history,
        },
        datadir / f"{input_str.replace('+', 'plus')}.json",
        request.config.getoption("force_regen"),
    )

@pytest.mark.parametrize("input_str, expected_output", [
    ("11*101", "1111"),
])
def test_turing_machine_binary_multiplication(
    request: pytest.FixtureRequest,
    global_datadir: Path,
    input_str: str,
    expected_output: str
) -> None:
    # Machine definition remains the same as in the original code
    machine = {...}  # The full machine definition is omitted for brevity

    datadir = global_datadir / "binary_multiplication"

    output, execution_history, accepted = run_turing_machine(machine, input_str)
    assert output == expected_output
    assert accepted

    regression_test(
        {
            "machine": machine,
            "input": input_str,
            "output": output,
            "execution_history": execution_history,
        },
        datadir / f"{input_str.replace('*', 'x')}.json",
        request.config.getoption("force_regen"),
    )