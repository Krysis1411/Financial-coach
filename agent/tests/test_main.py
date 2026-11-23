from types import SimpleNamespace

import pytest

import main
from main import FINANCIAL_DATA_KEY, DEFAULT_FINANCIAL_DATA, _normalize_category, _user_id_from_input, update_financial_data


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("rent", "Housing"),
        ("Groceries", "Food"),
        ("gas-bill", "Utilities"),
        ("  Medical ", "Healthcare"),
        ("Food", "Food"),
        ("something-unknown", "Other"),
        ("", "Other"),
    ],
)
def test_normalize_category(raw, expected):
    assert _normalize_category(raw) == expected


def _ctx(state=None):
    return SimpleNamespace(state=state if state is not None else {})


def test_update_sets_income_and_dependants():
    ctx = _ctx()
    result = update_financial_data(ctx, monthly_income=8000, dependants=2)
    fd = ctx.state[FINANCIAL_DATA_KEY]
    assert fd["monthly_income"] == 8000.0
    assert fd["dependants"] == 2
    assert result["status"] == "updated"


def test_expenses_patch_merges_and_normalizes_aliases():
    ctx = _ctx({FINANCIAL_DATA_KEY: {**DEFAULT_FINANCIAL_DATA, "manual_expenses": {"Food": 300.0}}})
    update_financial_data(ctx, expenses_patch={"rent": 2400, "groceries": 700})
    expenses = ctx.state[FINANCIAL_DATA_KEY]["manual_expenses"]
    assert expenses == {"Food": 700.0, "Housing": 2400.0}


def test_add_debts_appends_to_existing_list():
    ctx = _ctx()
    update_financial_data(ctx, add_debts=[{"name": "Car", "amount": 5000, "interest_rate": 6}])
    update_financial_data(ctx, add_debts=[{"name": "Card", "amount": 900, "interest_rate": 24.9}])
    names = [d["name"] for d in ctx.state[FINANCIAL_DATA_KEY]["debts"]]
    assert names == ["Car", "Card"]


def test_remove_debt_is_case_insensitive():
    ctx = _ctx()
    update_financial_data(ctx, add_debts=[{"name": "Student Loan", "amount": 1000, "interest_rate": 5}])
    result = update_financial_data(ctx, remove_debt_names=["student loan"])
    assert ctx.state[FINANCIAL_DATA_KEY]["debts"] == []
    assert any("removed" in change for change in result["changes"])


def test_noop_reports_no_op():
    result = update_financial_data(_ctx())
    assert result["changes"] == ["no-op"]


def test_user_id_accepts_valid_uuid():
    run_input = SimpleNamespace(forwarded_props={"userId": "3f2b8c1e-9a4d-4e7b-8f10-1234567890ab"})
    assert _user_id_from_input(run_input) == "3f2b8c1e-9a4d-4e7b-8f10-1234567890ab"


@pytest.mark.parametrize(
    "forwarded_props",
    [None, {}, {"userId": ""}, {"userId": "short"}, {"userId": "has spaces in it!"}, {"userId": 12345678}],
)
def test_user_id_rejects_missing_or_invalid(forwarded_props):
    with pytest.raises(ValueError):
        _user_id_from_input(SimpleNamespace(forwarded_props=forwarded_props))


def test_financial_data_key_is_user_scoped():
    assert main.FINANCIAL_DATA_KEY.startswith("user:")
