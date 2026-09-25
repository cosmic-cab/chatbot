import json
from pathlib import Path
import pytest

from eval.agent_runner import run_agent_and_capture_trace
from eval.eval_judge import llm_judge_accuracy


def load_all_test_cases():
    cases_dir = Path(__file__).parent / "test_cases"
    all_cases = []
    
    for json_file in cases_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_cases.extend(data)
            
    return all_cases


def save_test_trace(test_case: dict, agent_trace: dict, judge_result: dict):
    category = test_case.get("category", "uncategorized")
    category_dir = Path(__file__).parent / "traces" / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    trace_file = category_dir / f"trace_{test_case['id']}.json"
    
    trace_payload = {
        "test_case": test_case,
        "agent_execution_trace": {
            "executed_tools": agent_trace.get("executed_tools", []),
            "tool_calls_detail": agent_trace.get("tool_calls_detail", []),  # <--- Included SQL query content here
            "tool_outputs": agent_trace.get("tool_outputs", []),
            "final_response": agent_trace.get("final_response", "")
        },
        "llm_judge_evaluation": judge_result
    }
    
    with open(trace_file, "w", encoding="utf-8") as f:
        json.dump(trace_payload, f, indent=2, ensure_ascii=False)


TEST_CASES = load_all_test_cases()


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc["id"] for tc in TEST_CASES])
def test_agent_behavior(test_case):
    trace = run_agent_and_capture_trace(test_case["prompt"], thread_id=f"test_{test_case['id']}")
    
    judge_result = {
        "evaluated": False,
        "passed": None,
        "reasoning": "N/A - Deterministic Tool Selection Test"
    }

    try:
        # 1. Evaluate Tool Selection
        if test_case["category"] == "tool_selection":
            missing_tools = [
                tool for tool in test_case["expected_tools"] 
                if tool not in trace["executed_tools"]
            ]
            unexpected_tools = []
            if not test_case["expected_tools"] and len(trace["executed_tools"]) > 0:
                unexpected_tools = trace["executed_tools"]
                
            passed = len(missing_tools) == 0 and len(unexpected_tools) == 0
            reasoning = f"Expected tools: {test_case['expected_tools']}, Executed tools: {trace['executed_tools']}"
            
            judge_result = {
                "evaluated": True,
                "type": "deterministic_tool_check",
                "passed": passed,
                "reasoning": reasoning
            }
            assert passed, f"Failed {test_case['id']}: {reasoning}"

        # 2. Evaluate Synthesis Accuracy & Safety via LLM Judge
        if test_case["category"] in ["synthesis_accuracy", "safety"]:
            passed, reasoning = llm_judge_accuracy(
                prompt=test_case["prompt"],
                response=trace["final_response"],
                criteria=test_case["criteria"],
                executed_tools=trace["executed_tools"],
                tool_calls_detail=trace.get("tool_calls_detail", []),
                tool_outputs=trace["tool_outputs"]
            )
            
            judge_result = {
                "evaluated": True,
                "type": "llm_judge_reasoning",
                "passed": passed,
                "reasoning": reasoning
            }
            assert passed, f"Failed {test_case['id']}\nReasoning: {reasoning}\nActual Response: {trace['final_response']}"

    finally:
        save_test_trace(
            test_case=test_case,
            agent_trace=trace,
            judge_result=judge_result
        )