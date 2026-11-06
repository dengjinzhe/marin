# Copyright The Marin Authors
# SPDX-License-Identifier: Apache-2.0

import pytest
from verifyit.candidate import grade_candidate
from verifyit.reasoning_markup import ReasoningReply
from verifyit.spec import ReasoningMarkupSpec


@pytest.mark.parametrize(
    "reply,stop_reason,reward,violation",
    [
        ("<|start_think|>plan<|end_think|>ls -la", "stop", 1.0, None),
        ("Plain reply without any reasoning markers.", "stop", 1.0, None),
        ("<|start_think|>plan<|end_think|>text<|end_think|>more", "stop", 0.0, "stray_end"),
        ("<|start_think|>one<|end_think|><|start_think|>two<|end_think|>", "stop", 0.0, "second_span"),
        ("<|start_think|>never closed", "stop", 0.0, "unclosed"),
        ("plan<|end_think|>ls", "tool_calls", 0.0, "stray_end"),
        ("<|start_think|>still planning", "length", 1.0, None),
    ],
)
def test_reasoning_markup_scores_well_formed_spans_and_names_violations(reply, stop_reason, reward, violation):
    verdict = grade_candidate(ReasoningMarkupSpec(), ReasoningReply(reply, stop_reason), {})
    assert (verdict.reward, verdict.detail["violation"]) == (reward, violation)


def test_reasoning_markup_scores_an_empty_reply_zero_by_default():
    assert grade_candidate(ReasoningMarkupSpec(), ReasoningReply("", "stop"), {}).reward == 0.0
