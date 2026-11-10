# Placeholder handlers, one per route. Real inference comes from Cluster later.


def run_code(query: str) -> str:
    return f"[CODE MODEL] {query}"


def run_talk(query: str) -> str:
    return f"[TALK MODEL] {query}"


def run_refine(query: str) -> str:
    # Refine is two steps: one model drafts, a second improves the draft
    draft = f"[DRAFT] {query}"
    return f"[REFINED] {draft}"


HANDLERS = {"code": run_code, "talk": run_talk, "refine": run_refine}
