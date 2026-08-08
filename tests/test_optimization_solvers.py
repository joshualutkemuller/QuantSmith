"""Acceptance tests for spec 0013 — optimization solvers by mathematical form.

Each test is named for the acceptance criterion it covers (see
``specs/0013-optimization-solvers/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import math

from quantsmith.pipelines.optimization_solvers import (
    DPProblem,
    min_cost_flow,
    solve_dp,
    solve_lp,
    solve_milp,
)


# --- AC-001: LP solves to the known optimum ---


def test_lp_optimum_AC_001():
    # maximize x + y s.t. x<=4, y<=3, x+y<=5  -> objective 5
    r = solve_lp([1, 1], A_ub=[[1, 0], [0, 1], [1, 1]], b_ub=[4, 3, 5], sense="max")
    assert r.status == "optimal"
    assert math.isclose(r.objective, 5.0, abs_tol=1e-6)

    # minimize 2x + 3y s.t. x+y>=10, x<=8  -> 22 at (8, 2)
    r2 = solve_lp([2, 3], A_ub=[[-1, -1], [1, 0]], b_ub=[-10, 8], sense="min")
    assert r2.status == "optimal"
    assert math.isclose(r2.objective, 22.0, abs_tol=1e-6)
    assert math.isclose(r2.x[0], 8.0, abs_tol=1e-6)


# --- AC-002: LP reports infeasible and unbounded explicitly ---


def test_lp_infeasible_and_unbounded_AC_002():
    # x<=1 and x>=2 -> infeasible
    assert solve_lp([1], A_ub=[[1], [-1]], b_ub=[1, -2]).status == "infeasible"
    # maximize x with only x>=0 -> unbounded
    assert solve_lp([1], A_ub=[[-1]], b_ub=[0], sense="max").status == "unbounded"


# --- AC-003: MILP returns integer solutions and beats/matches the relaxation bound ---


def test_milp_integer_solution_AC_003():
    # 0/1 knapsack: max 6a + 5b s.t. 3a + 4b <= 6, a,b in {0,1}
    r = solve_milp(
        [6, 5],
        A_ub=[[3, 4], [1, 0], [0, 1]],
        b_ub=[6, 1, 1],
        integer_vars=[0, 1],
        sense="max",
    )
    assert r.status == "optimal"
    assert r.x == [1, 0]
    assert math.isclose(r.objective, 6.0, abs_tol=1e-6)
    # Every integer var is integral.
    for v in r.x:
        assert abs(v - round(v)) < 1e-9

    # An LP fractional optimum is tightened to an integer one.
    frac = solve_lp([1], A_ub=[[2]], b_ub=[3], sense="max")  # x <= 1.5 -> 1.5
    assert math.isclose(frac.objective, 1.5, abs_tol=1e-6)
    integral = solve_milp([1], A_ub=[[2]], b_ub=[3], integer_vars=[0], sense="max")
    assert integral.x == [1]


# --- AC-004: min-cost flow finds the min-cost max flow ---


def test_min_cost_flow_AC_004():
    # Diamond network 0 -> {1,2} -> 3.
    edges = [
        (0, 1, 3, 1),
        (0, 2, 2, 2),
        (1, 3, 2, 1),
        (2, 3, 3, 1),
        (1, 2, 1, 1),
    ]
    f = min_cost_flow(4, edges, source=0, sink=3)
    assert f.status == "optimal"
    assert math.isclose(f.flow, 5.0, abs_tol=1e-6)   # both source arcs saturated
    assert math.isclose(f.cost, 13.0, abs_tol=1e-6)

    # A required flow beyond capacity is infeasible.
    infeasible = min_cost_flow(4, edges, source=0, sink=3, required_flow=6.0)
    assert infeasible.status == "infeasible"


# --- AC-005: DP backward induction returns the optimal value/policy ---


def test_dp_backward_induction_AC_005():
    # Two stages; reward = current state each stage; minimize -> stay at 0.
    def actions(s):
        return [0, 1]

    def step(s, a):
        return min(s + a, 2), float(s)

    res = solve_dp(DPProblem(horizon=2, states=[0, 1, 2], actions=actions, step=step, sense="min"))
    assert math.isclose(res.values[0], 0.0, abs_tol=1e-9)
    # From state 0, the optimal first action is to not increase.
    assert res.policy[(0, 0)] == 0

    # Maximize variant: reward = current state -> climb to 2.
    def step_gain(s, a):
        return min(s + a, 2), float(s)

    res2 = solve_dp(DPProblem(horizon=3, states=[0, 1, 2], actions=actions, step=step_gain, sense="max"))
    assert res2.values[2] >= res2.values[0]


# --- AC-006: deterministic ---


def test_deterministic_AC_006():
    a = solve_lp([1, 1], A_ub=[[1, 0], [0, 1], [1, 1]], b_ub=[4, 3, 5], sense="max")
    b = solve_lp([1, 1], A_ub=[[1, 0], [0, 1], [1, 1]], b_ub=[4, 3, 5], sense="max")
    assert a == b
    edges = [(0, 1, 3, 1), (1, 2, 3, 1)]
    assert min_cost_flow(3, edges, 0, 2) == min_cost_flow(3, edges, 0, 2)
