#!/usr/bin/env python3
"""Lint a Layer 1 Agent Spec produced by ax-agent-spec.

Usage:
    python lint_spec.py <spec.md>
    python lint_spec.py --self-test

Stdlib only. Exit codes:
    0 - clean
    1 - one or more violations (each printed)
    2 - usage / file error
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ---------- Vocabularies -----------------------------------------------------

STATUS_VALUES: Set[str] = {
    "ANSWERED", "PARTIAL", "MISSING", "SPIKE",
    "DEFERRED-L2", "DEFERRED-L3",
}
MECHANISMS: Set[str] = {"action", "flow", "prompt"}
CANDIDATE_TYPES: Set[str] = {"would-match-seeded-standard", "harvested"}

P0_ROW_NAMES: Dict[int, str] = {
    1: "Goal + non-goals",
    2: "Primary user & their goal",
    3: "Trigger / entry point",
    4: "Channel",
    5: "Subagent inventory",
    6: "Action inventory",
    7: "Execution mechanism & feasibility",
    8: "Data read/written + Variables Block",
    9: "Guardrails / must-nevers, with placement",
    10: "Failure & recovery + global messages",
    11: "Human escalation / handoff",
    12: "Success metrics",
    13: "v1 scope boundary + open spikes",
}
AGENT_ROWS: Set[int] = {1, 2, 3, 4, 9, 10, 11, 12, 13}
SUBAGENT_ROWS: Set[int] = {6, 7, 8}

DEFAULT_TAXONOMY: Set[str] = {
    "human-in-the-loop", "fallback", "escalation-to-human",
    "confirmation", "disambiguation",
    "golden-path-ordering", "act-without-confirm", "missing-fallback",
    "assumption-without-intent", "capability-gap-masking",
    "late-or-missing-escalation",
    "sensitive-data-disclosure", "identity-verification",
    "identity-verification/patient", "identity-verification/payer",
    "identity-verification/provider", "irreversible-action-confirmation",
}


# ---------- Regexes ----------------------------------------------------------

H2_SECTION = re.compile(
    r"^##\s+(\d+)\.\s+(.+?)\s+—\s+\[([A-Z0-9\- ]+?)\]\s*$"
)
H1_SUBAGENT = re.compile(
    r"^#\s+Subagent:\s+SA-(\d+)\s+—\s+(.+?)\s+\[archetype:\s+([A-Z\-]+)\]\s*$",
    re.IGNORECASE,
)
H1_HEADING = re.compile(r"^#\s+(.+?)\s*$")
TITLE_FIELD = re.compile(r"^\*\*([A-Za-z][^:]*?):\*\*\s+(.+?)\s*$")
SPIKE_REF = re.compile(r"\bS-(\d+)\b")
TOPIC_WORD = re.compile(r"\btopic\b", re.IGNORECASE)
FORMERLY_TOPIC = re.compile(r"formerly\s+topic", re.IGNORECASE)
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
MANIFEST_ROW = re.compile(r"^(\d+)\.\s+(.+?)(\s+—\s+SA-(\d+))?\s*$")
ACTION_ID = re.compile(r"^\d+\.\d+$")


def parse_table_row(line: str) -> Optional[List[str]]:
    """Return table cells, or None if not a data row."""
    m = TABLE_ROW.match(line)
    if not m:
        return None
    cells = [c.strip() for c in m.group(1).split("|")]
    if cells and all(re.match(r"^:?-+:?$", c) for c in cells if c):
        return None
    return cells


# ---------- Parsed structures ------------------------------------------------

@dataclass
class Section:
    row_num: int
    name: str
    status: str
    body: List[str]
    line_num: int
    subagent: Optional[int] = None


@dataclass
class ManifestRow:
    row_num: int
    name: str
    scope: str
    status: str
    notes: str
    subagent: Optional[int]
    line_num: int


@dataclass
class Spike:
    spike_id: str
    owner: str
    priority: str
    line_num: int


@dataclass
class PatternCandidate:
    situation: str
    mechanism: str
    subagent_ref: str
    candidate_type: str
    note: str
    line_num: int


@dataclass
class ParsedSpec:
    raw: str = ""
    lines: List[str] = field(default_factory=list)
    version: str = ""
    team: str = ""
    product_owner: str = ""
    primitives_version: str = ""
    primitives_verified: str = ""
    manifest_rows: List[ManifestRow] = field(default_factory=list)
    sections: List[Section] = field(default_factory=list)
    subagents: List[int] = field(default_factory=list)
    action_ids_by_subagent: Dict[int, List[str]] = field(default_factory=dict)
    spikes: List[Spike] = field(default_factory=list)
    spike_refs: List[Tuple[str, int]] = field(default_factory=list)
    pattern_candidates: List[PatternCandidate] = field(default_factory=list)
    changelog_versions: List[str] = field(default_factory=list)


# ---------- Parser -----------------------------------------------------------

def parse_spec(text: str) -> ParsedSpec:
    spec = ParsedSpec(raw=text, lines=text.splitlines())

    # Title block (scan top ~60 lines).
    for line in spec.lines[:60]:
        if line.startswith("# ") and "Agent Spec" in line:
            continue
        m = TITLE_FIELD.match(line)
        if not m:
            continue
        name = m.group(1).strip()
        value = m.group(2).strip()
        if name == "Version":
            spec.version = value
        elif name == "Team":
            spec.team = value
        elif name.startswith("Product Owner"):
            spec.product_owner = value
        elif name == "Primitives version":
            pv = re.match(r"(\S+)\s+\(last_verified\s+(\S+)\)", value)
            if pv:
                spec.primitives_version = pv.group(1)
                spec.primitives_verified = pv.group(2)
            else:
                spec.primitives_version = value

    # Walk the body.
    current_subagent: Optional[int] = None
    current_section: Optional[Section] = None
    in_manifest = False
    in_rubric = False
    in_patterns = False
    in_changelog = False
    in_spike_log = False

    for i, line in enumerate(spec.lines):
        # H1 — Subagent block boundary
        sa = H1_SUBAGENT.match(line)
        if sa:
            current_subagent = int(sa.group(1))
            if current_subagent not in spec.subagents:
                spec.subagents.append(current_subagent)
            current_section = None
            in_spike_log = False
            in_manifest = False
            continue

        # Any other H1 ends section + subagent context
        h1 = H1_HEADING.match(line)
        if h1:
            heading = h1.group(1).strip().lower()
            current_section = None
            current_subagent = None
            in_manifest = False
            in_rubric = in_patterns = in_changelog = False
            in_spike_log = (heading == "spike log")
            continue

        # H2 — numbered rubric section
        sec_m = H2_SECTION.match(line)
        if sec_m:
            row_num = int(sec_m.group(1))
            section = Section(
                row_num=row_num,
                name=sec_m.group(2).strip(),
                status=sec_m.group(3).strip(),
                body=[],
                line_num=i + 1,
                subagent=current_subagent if row_num in SUBAGENT_ROWS else None,
            )
            spec.sections.append(section)
            current_section = section
            in_manifest = False
            in_rubric = in_patterns = in_changelog = False
            continue

        # Body capture (until next heading)
        if current_section is not None:
            if line.startswith("#"):
                current_section = None
            else:
                current_section.body.append(line)

        # Manifest detection
        if line.strip() == "## Completion manifest":
            in_manifest = True
            continue
        if in_manifest and line.startswith("### "):
            sub = line.lstrip("# ").strip().lower()
            in_rubric = sub.startswith("rubric coverage")
            in_patterns = sub.startswith("pattern candidates")
            in_changelog = sub.startswith("changelog")
            continue

        # Manifest table parsing
        if in_manifest:
            cells = parse_table_row(line)
            if cells is None or not cells:
                continue
            first_lower = cells[0].strip().lower()
            # skip header rows
            if first_lower in {
                "rubric row", "situation", "version", "id",
                "document", "spike id",
            }:
                continue

            if in_rubric and len(cells) >= 3:
                mm = MANIFEST_ROW.match(cells[0])
                if mm:
                    spec.manifest_rows.append(ManifestRow(
                        row_num=int(mm.group(1)),
                        name=mm.group(2).strip(),
                        scope=cells[1],
                        status=cells[2],
                        notes=cells[3] if len(cells) > 3 else "",
                        subagent=int(mm.group(4)) if mm.group(4) else None,
                        line_num=i + 1,
                    ))
            elif in_patterns and len(cells) >= 5:
                situation = cells[0]
                if situation.startswith("<") or situation.startswith("("):
                    continue
                spec.pattern_candidates.append(PatternCandidate(
                    situation=situation,
                    mechanism=cells[1],
                    subagent_ref=cells[2],
                    candidate_type=cells[3],
                    note=cells[4],
                    line_num=i + 1,
                ))
            elif in_changelog and len(cells) >= 1:
                ver = cells[0]
                if ver and not ver.startswith("<"):
                    spec.changelog_versions.append(ver)

        # Spike log
        if in_spike_log:
            cells = parse_table_row(line)
            if cells is None or not cells:
                pass
            elif cells[0].startswith("S-") and len(cells) >= 3:
                spec.spikes.append(Spike(
                    spike_id=cells[0],
                    owner=cells[1],
                    priority=cells[2],
                    line_num=i + 1,
                ))

        # Spike references everywhere
        for m in SPIKE_REF.finditer(line):
            spec.spike_refs.append((m.group(0), i + 1))

    # Action IDs per subagent — from row 6 and row 7 tables
    for sec in spec.sections:
        if sec.row_num in {6, 7} and sec.subagent is not None:
            for body_line in sec.body:
                cells = parse_table_row(body_line)
                if not cells:
                    continue
                if ACTION_ID.match(cells[0]):
                    spec.action_ids_by_subagent.setdefault(
                        sec.subagent, []).append(cells[0])

    return spec


# ---------- Taxonomy loader --------------------------------------------------

def load_taxonomy(path: Optional[Path]) -> Set[str]:
    if path is None or not path.exists():
        return DEFAULT_TAXONOMY
    text = path.read_text()
    found: Set[str] = set()
    # Bullet items of the form: `- **slug** — description`
    for m in re.finditer(r"^\s*-\s+\*\*([a-z0-9\-/]+)\*\*\s+—",
                         text, re.MULTILINE):
        found.add(m.group(1))
    # Persona variants surfaced inline as `identity-verification/<persona>`
    for m in re.finditer(r"`(identity-verification/[a-z]+)`", text):
        found.add(m.group(1))
    return found if len(found) >= 5 else DEFAULT_TAXONOMY


# ---------- Checks -----------------------------------------------------------

def _tag(row_num: int, sa: Optional[int]) -> str:
    return f"row {row_num}" + (f" SA-{sa}" if sa else "")


def check_1_sections_present(spec: ParsedSpec) -> List[str]:
    """13 rubric sections in order; subagent rows repeat per subagent."""
    fails: List[str] = []
    expected: List[Tuple[int, Optional[int]]] = []
    for row in (1, 2, 3, 4, 5):
        expected.append((row, None))
    for sa in spec.subagents:
        for row in (6, 7, 8):
            expected.append((row, sa))
    for row in (9, 10, 11, 12, 13):
        expected.append((row, None))
    actual = [(s.row_num, s.subagent) for s in spec.sections]
    if actual == expected:
        return fails
    exp_set, act_set = set(expected), set(actual)
    for k in sorted(exp_set - act_set):
        fails.append(f"[Check 1] Missing section {_tag(*k)}")
    for k in sorted(act_set - exp_set):
        fails.append(f"[Check 1] Unexpected section {_tag(*k)}")
    if exp_set == act_set and actual != expected:
        fails.append("[Check 1] Sections present but out of expected order")
    return fails


def check_2_manifest(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    if not spec.manifest_rows:
        return ["[Check 2] Manifest table missing or unparseable"]
    expected: Set[Tuple[int, Optional[int]]] = set()
    for row in AGENT_ROWS | {5}:
        expected.add((row, None))
    for sa in spec.subagents:
        for row in SUBAGENT_ROWS:
            expected.add((row, sa))
    actual = {(m.row_num, m.subagent) for m in spec.manifest_rows}
    for k in sorted(expected - actual):
        fails.append(f"[Check 2] Manifest missing {_tag(*k)}")
    return fails


def check_3_inline_vs_manifest(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    idx = {(m.row_num, m.subagent): m for m in spec.manifest_rows}
    for sec in spec.sections:
        key = (sec.row_num,
               sec.subagent if sec.row_num in SUBAGENT_ROWS else None)
        m = idx.get(key)
        if m is None:
            continue
        if sec.status.strip() != m.status.strip():
            fails.append(
                f"[Check 3] {_tag(sec.row_num, sec.subagent)} inline "
                f"[{sec.status}] disagrees with manifest '{m.status}' "
                f"(line {sec.line_num})")
    return fails


def check_4_status_vocab(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    for sec in spec.sections:
        head = sec.status.split()[0] if sec.status else ""
        if head not in STATUS_VALUES:
            fails.append(
                f"[Check 4] Section row {sec.row_num} invalid status "
                f"'{sec.status}' (line {sec.line_num})")
    for m in spec.manifest_rows:
        if not m.status:
            continue
        head = m.status.split()[0]
        if head not in STATUS_VALUES:
            fails.append(
                f"[Check 4] Manifest row {m.row_num} invalid status "
                f"'{m.status}' (line {m.line_num})")
    return fails


def check_5_numbering(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    if spec.subagents:
        expected = list(range(1, len(spec.subagents) + 1))
        if spec.subagents != expected:
            fails.append(
                f"[Check 5] Subagent IDs not contiguous SA-1..SA-N: "
                f"got {spec.subagents}")
    for sa, action_ids in spec.action_ids_by_subagent.items():
        for aid in action_ids:
            parent = int(aid.split(".")[0])
            if parent != sa:
                fails.append(
                    f"[Check 5] Action {aid} under SA-{sa} has wrong "
                    f"parent (expected {sa}.X)")
    return fails


def check_6_spikes(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    ids = {s.spike_id for s in spec.spikes}
    seen: Set[str] = set()
    for ref, line in spec.spike_refs:
        if ref in seen:
            continue
        seen.add(ref)
        # ignore references inside the spike log itself
        in_log = any(s.line_num == line for s in spec.spikes)
        if in_log:
            continue
        if ref not in ids:
            fails.append(
                f"[Check 6] {ref} referenced but absent from spike log "
                f"(first ref line {line})")
    for s in spec.spikes:
        if not s.owner or s.owner.startswith("<"):
            fails.append(
                f"[Check 6] {s.spike_id} missing owner role "
                f"(line {s.line_num})")
        prio = s.priority.strip()
        if prio.startswith("<") or not prio:
            fails.append(
                f"[Check 6] {s.spike_id} missing priority "
                f"(line {s.line_num})")
        elif "P0" not in prio and "P1" not in prio:
            fails.append(
                f"[Check 6] {s.spike_id} invalid priority '{prio}' "
                f"(line {s.line_num})")
        elif "/" in prio:  # unresolved template "P0 / P1"
            fails.append(
                f"[Check 6] {s.spike_id} priority unresolved '{prio}' "
                f"(line {s.line_num})")
    return fails


def check_7_title_changelog(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    if not spec.version:
        fails.append("[Check 7] Title block missing Version")
    if not spec.primitives_version:
        fails.append("[Check 7] Title block missing Primitives version")
    if not spec.team:
        fails.append("[Check 7] Title block missing Team")
    if not spec.product_owner:
        fails.append("[Check 7] Title block missing Product Owner")
    if spec.version and spec.version not in spec.changelog_versions:
        fails.append(
            f"[Check 7] Changelog has no entry for document Version "
            f"'{spec.version}' (changelog: {spec.changelog_versions})")
    return fails


def check_8_no_topic(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    for i, line in enumerate(spec.lines):
        scrubbed = FORMERLY_TOPIC.sub("", line)
        m = TOPIC_WORD.search(scrubbed)
        if m:
            fails.append(
                f"[Check 8] 'topic' appears at line {i + 1} outside "
                f"literal 'formerly topic': {line.strip()!r}")
    return fails


def check_9_no_empty(spec: ParsedSpec) -> List[str]:
    fails: List[str] = []
    for sec in spec.sections:
        non_blank = [b for b in sec.body if b.strip()]
        if not non_blank:
            fails.append(
                f"[Check 9] Section row {sec.row_num} "
                f"(line {sec.line_num}) has empty body")
            continue
        head = sec.status.split()[0] if sec.status else ""
        if head in {"MISSING", "PARTIAL", "SPIKE"}:
            joined = "\n".join(sec.body)
            if "?" not in joined and "Challenge" not in joined:
                fails.append(
                    f"[Check 9] Section row {sec.row_num} status {head} "
                    f"lacks a pre-printed challenge question "
                    f"(line {sec.line_num})")
    return fails


def check_10_pattern_candidates(
    spec: ParsedSpec, taxonomy: Set[str]
) -> List[str]:
    fails: List[str] = []
    for pc in spec.pattern_candidates:
        if pc.situation not in taxonomy:
            fails.append(
                f"[Check 10] Situation '{pc.situation}' not in "
                f"situation-taxonomy.md (line {pc.line_num})")
        if pc.mechanism not in MECHANISMS:
            fails.append(
                f"[Check 10] Mechanism '{pc.mechanism}' not in "
                f"{{action, flow, prompt}} (line {pc.line_num})")
        if pc.candidate_type not in CANDIDATE_TYPES:
            fails.append(
                f"[Check 10] Candidate-type '{pc.candidate_type}' not in "
                f"{{would-match-seeded-standard, harvested}} "
                f"(line {pc.line_num})")
        if not re.match(r"^SA-\d+$", pc.subagent_ref):
            fails.append(
                f"[Check 10] Subagent ref '{pc.subagent_ref}' not "
                f"SA-N format (line {pc.line_num})")
    return fails


# ---------- Runner -----------------------------------------------------------

def lint_file(path: Path, taxonomy_path: Optional[Path] = None) -> List[str]:
    text = path.read_text()
    spec = parse_spec(text)
    tax = load_taxonomy(taxonomy_path)
    fails: List[str] = []
    fails += check_1_sections_present(spec)
    fails += check_2_manifest(spec)
    fails += check_3_inline_vs_manifest(spec)
    fails += check_4_status_vocab(spec)
    fails += check_5_numbering(spec)
    fails += check_6_spikes(spec)
    fails += check_7_title_changelog(spec)
    fails += check_8_no_topic(spec)
    fails += check_9_no_empty(spec)
    fails += check_10_pattern_candidates(spec, tax)
    return fails


def default_taxonomy_path() -> Path:
    return (Path(__file__).resolve().parent.parent
            / "references" / "situation-taxonomy.md")


CHECK_NUM = re.compile(r"\[Check (\d+)\]")
EXPECTED_BROKEN_CHECKS: Set[str] = {"3", "6", "7", "8", "10"}


def self_test() -> int:
    here = Path(__file__).resolve().parent
    fixtures = here / "fixtures"
    if not fixtures.exists():
        print(f"self-test ERROR: fixtures dir {fixtures} missing",
              file=sys.stderr)
        return 2
    passing = fixtures / "passing-spec.md"
    broken = fixtures / "broken-spec.md"
    taxonomy = default_taxonomy_path()

    rc = 0
    print("=== ax-agent-spec lint self-test ===")

    if passing.exists():
        f = lint_file(passing, taxonomy)
        if f:
            print(f"FAIL: {passing.name} should be clean — got:")
            for line in f:
                print(f"  {line}")
            rc = 1
        else:
            print(f"PASS: {passing.name} lints clean")
    else:
        print(f"SKIP: {passing.name} missing")
        rc = 2

    if broken.exists():
        f = lint_file(broken, taxonomy)
        if not f:
            print(f"FAIL: {broken.name} should have violations")
            rc = 1
        else:
            seen = {CHECK_NUM.search(x).group(1)
                    for x in f if CHECK_NUM.search(x)}
            missing = EXPECTED_BROKEN_CHECKS - seen
            if missing:
                print(f"FAIL: {broken.name} did not trigger expected "
                      f"checks {sorted(missing)} — got {sorted(seen)}")
                rc = 1
            else:
                print(f"PASS: {broken.name} triggered "
                      f"{len(f)} violation(s) across "
                      f"checks {sorted(seen)}:")
                for line in f:
                    print(f"  {line}")
    else:
        print(f"SKIP: {broken.name} missing")
        rc = 2

    return rc


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("usage: lint_spec.py <spec.md>  |  lint_spec.py --self-test",
              file=sys.stderr)
        return 2
    if argv[1] == "--self-test":
        return self_test()
    path = Path(argv[1])
    if not path.exists():
        print(f"error: {path} not found", file=sys.stderr)
        return 2
    fails = lint_file(path, default_taxonomy_path())
    if fails:
        print(f"{len(fails)} violation(s) in {path}:")
        for line in fails:
            print(f"  {line}")
        return 1
    print(f"OK: {path} lints clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
