#!/usr/bin/env python3
"""
Detect work type from user prompts and inject appropriate guidance.

This hook runs on UserPromptSubmit and analyzes the prompt for keywords
that indicate a specific type of work (bugfix, refactor, optimization, etc.).
When detected, it injects context telling Claude to apply the relevant guidance.
"""

import sys
import json
import re

def detect_work_types(prompt: str) -> list[str]:
    """
    Detect all matching work types from prompt text.
    Returns list of work types that matched, or empty list if none.
    """
    prompt_lower = prompt.lower()

    patterns = {
        "greenfield": [
            r"\bnew project\b",
            r"\bfrom scratch\b",
            r"\bbootstrap\b",
            r"\bscaffold\b",
            r"\binitialize\b",
            r"\bstart fresh\b",
            r"\bgreenfield\b",
        ],
        "integration": [
            r"\bintegrat(e|ion|ing)\b",
            r"\bexternal (api|service)\b",
            r"\bthird[- ]party\b",
            r"\bwebhook\b",
            r"\bconnect to\b",
            r"\bsync with\b",
            r"\bapi (integration|client)\b",
        ],
        "bugfix": [
            r"\bbug\b",
            r"\bfix(ing|ed)?\b(?!ture)",  # fix but not fixture
            r"\bbroken\b",
            r"\bdoesn'?t work\b",
            r"\bnot working\b",
            r"\berror\b",
            r"\bissue\b",
            r"\bcrash(ing|ed|es)?\b",
            r"\bfailing\b",
            r"\bdebug\b",
            r"\bdefect\b",
            r"\bwrong\b",
            r"\bincorrect\b",
            r"\bregression\b",
        ],
        "refactor": [
            r"\brefactor\b",
            r"\brestructur(e|ing)\b",
            r"\breorganiz(e|ing)\b",
            r"\bclean(ing)? up\b",
            r"\bextract (function|method|class|component|module)\b",
            r"\brename\b",
            r"\bconsolidat(e|ing)\b",
            r"\bsimplif(y|ying)\b",
            r"\bdedup(licate)?\b",
            r"\breduc(e|ing) (duplication|complexity)\b",
            r"\bmove (to|into)\b",
        ],
        "optimization": [
            r"\boptimiz(e|ing|ation)\b",
            r"\bperformance\b",
            r"\bslow(er)?\b",
            r"\bfast(er)?\b",
            r"\bspeed(ing)? up\b",
            r"\bmemory (usage|leak|consumption)\b",
            r"\befficient\b",
            r"\blatency\b",
            r"\bbottleneck\b",
            r"\bprofil(e|ing)\b",
            r"\bcach(e|ing)\b",
        ],
        "feature": [
            r"\badd(ing)? (a |the )?(new )?feature\b",
            r"\bimplement(ing)?\b",
            r"\bnew functionality\b",
            r"\bcreate (a |the )?(new )?(feature|component|module)\b",
            r"\bbuild(ing)? (a |the )?(new )?\b",
            r"\badd(ing)? support for\b",
            r"\benable\b",
            r"\bintroduc(e|ing)\b",
        ],
    }

    matched_types = []
    for work_type, keyword_patterns in patterns.items():
        for pattern in keyword_patterns:
            if re.search(pattern, prompt_lower):
                matched_types.append(work_type)
                break  # One match per type is enough

    return matched_types


def get_guidance_context(work_type: str) -> str:
    """Generate the context to inject for a given work type."""

    guidance_map = {
        "bugfix": """Apply BUGFIX guidance for this work:
- Understand root cause before fixing (obvious from code = fix directly; unclear = reproduce first)
- Minimal changes: fix the bug, don't refactor surrounding code
- Write a failing test first when practical
- Verify the fix doesn't introduce regressions
- Consider: could this bug exist elsewhere?

Reference: flow-skill/bugfix.md for detailed guidance.""",

        "refactor": """Apply REFACTOR guidance for this work:
- Behavior preservation is paramount - no functional changes
- Follow the loop: test -> change -> test -> commit -> repeat
- Make incremental changes, verify continuously
- Don't refactor and add features simultaneously
- Ensure adequate test coverage before risky refactors

Reference: flow-skill/refactor.md for detailed guidance.""",

        "optimization": """Apply OPTIMIZATION guidance for this work:
- Measure first - establish baseline before optimizing
- Profile don't guess - find actual bottlenecks
- One change at a time - isolate improvements
- Verify improvements with benchmarks
- 80/20 rule: focus on biggest impact first

Reference: flow-skill/optimization.md for detailed guidance.""",

        "feature": """Apply FEATURE development guidance for this work:
- Explore existing patterns before writing new code
- Maintain consistency with codebase conventions
- Integrate incrementally - small working pieces
- Consider edge cases and error handling
- Write tests alongside implementation

Reference: flow-skill/feature.md for detailed guidance.""",

        "integration": """Apply INTEGRATION guidance for this work:
- Understand the external system first (docs, API contracts)
- Design for failure: timeouts, retries, circuit breakers
- Isolate integration code (client layer, adapters)
- Test at boundaries with both mocked and real calls
- Handle auth, rate limiting, and schema changes

Reference: flow-skill/integration.md for detailed guidance.""",

        "greenfield": """Apply GREENFIELD project guidance for this work:
- Requirements first - clarify what success looks like
- Architecture before code - make foundational decisions explicit
- Validate early - get feedback on core assumptions
- Build for change - avoid premature optimization
- Set up infrastructure: testing, CI, documentation

Reference: flow-skill/greenfield.md for detailed guidance.""",
    }

    return guidance_map.get(work_type, "")


def main():
    try:
        # Read the prompt from stdin
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get("prompt", "")

        # Detect work types (can be multiple)
        work_types = detect_work_types(prompt)

        if work_types:
            # Gather guidance for all matched types
            all_guidance = [get_guidance_context(wt) for wt in work_types]

            context = f"""[Workflow guidance injected by hook]

{chr(10).join(all_guidance)}"""
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context
                }
            }
        else:
            # No match - continue without additional context
            output = {"continue": True}

        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        # On error, fail open - don't block the prompt
        sys.stderr.write(f"detect-workflow hook error: {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
