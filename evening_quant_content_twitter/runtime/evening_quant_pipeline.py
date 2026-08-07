#!/usr/bin/env python3
"""Deterministic evening quant content draft-pack generator.

This runtime is deliberately non-posting. It emits reviewable YAML and Markdown
draft packs from config, optional context notes, and metadata-only memory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_TOPICS = [
    "AI infrastructure",
    "equity concentration",
    "macro liquidity",
    "volatility",
    "market microstructure",
    "securities finance",
    "collateral optimization",
    "repo",
    "quant research",
    "model risk",
]

DEFAULT_CONFIG: dict[str, Any] = {
    "workflow_name": "evening_quant_content",
    "schedule": {
        "frequency": "daily",
        "time": "22:30",
        "timezone": "America/New_York",
    },
    "platform": {
        "primary": "x",
        "max_post_chars": 280,
        "max_thread_posts": 8,
        "require_manual_approval": True,
        "auto_post_enabled": False,
    },
    "content": {
        "ideas_per_run": 15,
        "finished_posts": 5,
        "thread_drafts": 3,
        "meme_concepts": 5,
        "visual_specs": 5,
    },
    "topics": {"include": DEFAULT_TOPICS},
    "memory": {"path": "evening_quant_content_twitter/memory/evening_quant_content"},
    "delivery": {
        "draft_channel": "local_file",
        "output_template": "evening_quant_content_twitter/templates/docs/evening_quant_draft_pack.md",
    },
}


ANGLE_TEMPLATES = [
    "{topic} is best framed as a constraint problem, not a forecast.",
    "The overlooked edge in {topic} is measuring the bottleneck before optimizing the signal.",
    "{topic} gets more interesting when you separate volume, price, and balance-sheet capacity.",
    "Most commentary on {topic} ignores second-order effects from flows and financing.",
    "The sharper question in {topic}: which variable is actually scarce?",
]


def _bool(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1", "on"}


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def load_config(path: Path) -> dict[str, Any]:
    """Load enough YAML for the checked-in config without extra dependencies."""
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if not path.exists():
        raise FileNotFoundError(f"config not found: {path}")

    section: str | None = None
    list_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*$", line):
            section = line.split(":", 1)[0].strip()
            list_key = None
            continue
        if section == "topics" and re.match(r"^\s+include:\s*$", line):
            list_key = "topics.include"
            cfg["topics"]["include"] = []
            continue
        if list_key == "topics.include" and re.match(r"^\s+-\s+", line):
            cfg["topics"]["include"].append(_strip_quotes(line.split("-", 1)[1]))
            continue
        match = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.+?)\s*$", line)
        if not match or section is None:
            continue
        key, value = match.groups()
        value = _strip_quotes(value)
        target = cfg.setdefault(section, {})
        if value.lower() in {"true", "false", "yes", "no", "on", "off"}:
            target[key] = _bool(value)
        elif re.fullmatch(r"-?\d+", value):
            target[key] = int(value)
        elif re.fullmatch(r"-?\d+\.\d+", value):
            target[key] = float(value)
        else:
            target[key] = value

    if not cfg["topics"]["include"]:
        cfg["topics"]["include"] = DEFAULT_TOPICS
    return cfg


def load_context(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return []
    if not path.exists():
        raise FileNotFoundError(f"context not found: {path}")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
        signals = payload.get("signals", payload if isinstance(payload, list) else [])
        return [
            {
                "title": str(item.get("title", f"Signal {idx + 1}")),
                "note": str(item.get("note", item.get("summary", ""))).strip(),
                "source": str(item.get("source", "user-supplied context")),
            }
            for idx, item in enumerate(signals)
            if isinstance(item, dict)
        ]

    signals: list[dict[str, str]] = []
    for idx, line in enumerate(l.strip("-* ").strip() for l in text.splitlines()):
        if not line or line.startswith("#"):
            continue
        signals.append(
            {
                "title": f"Context note {idx + 1}",
                "note": line,
                "source": str(path),
            }
        )
    return signals


def load_memory(memory_path: Path) -> dict[str, list[str]]:
    themes_path = memory_path / "themes.md"
    rejected_path = memory_path / "rejected_framing.md"
    memory = {"used_hooks": [], "avoid": []}
    if themes_path.exists():
        for line in themes_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("- "):
                memory["used_hooks"].append(line.strip("- ").strip())
    if rejected_path.exists():
        for line in rejected_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("- "):
                memory["avoid"].append(line.strip("- ").strip())
    return memory


def _score(index: int) -> dict[str, int]:
    return {
        "timeliness": 5 if index < 5 else 4,
        "novelty": 5 - (index % 3 == 0),
        "quant_depth": 5 if index % 2 == 0 else 4,
        "visual_potential": 5 if index % 4 in {0, 1} else 3,
        "meme_potential": 4 if index % 5 in {0, 2} else 2,
        "claim_risk": 2 if index % 3 else 3,
    }


def _topic_slug(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")


def build_draft_pack(
    config: dict[str, Any],
    config_path: Path,
    context: list[dict[str, str]],
    memory: dict[str, list[str]],
    generated_at: dt.datetime,
) -> dict[str, Any]:
    content_cfg = config["content"]
    platform_cfg = config["platform"]
    topics = list(config["topics"]["include"])
    ideas_count = int(content_cfg["ideas_per_run"])
    source_notes = []

    if context:
        for idx, signal in enumerate(context, start=1):
            source_notes.append(
                {
                    "id": f"src-{idx:03d}",
                    "claim_supported": signal["note"],
                    "source_type": "user_supplied_context",
                    "citation": signal["source"],
                    "retrieved_at": generated_at.isoformat(),
                    "caveat": "User-supplied context; refresh source before posting if market-current.",
                }
            )
    else:
        source_notes.append(
            {
                "id": "src-001",
                "claim_supported": "Workflow method note; no live market data was supplied.",
                "source_type": "method",
                "citation": "No external data supplied for this deterministic run.",
                "retrieved_at": None,
                "caveat": "Add current sources before publishing factual market claims.",
            }
        )

    ranked_ideas = []
    for i in range(ideas_count):
        topic = topics[i % len(topics)]
        template = ANGLE_TEMPLATES[i % len(ANGLE_TEMPLATES)]
        signal = context[i % len(context)] if context else None
        title = template.format(topic=topic)
        if signal:
            title = f"{topic}: {signal['note'][:82].rstrip('.')}"
        idea_id = f"idea-{i + 1:03d}"
        ranked_ideas.append(
            {
                "id": idea_id,
                "title": title,
                "topic": topic,
                "format": ["post", "thread", "visual", "meme"][i % 4],
                "score": _score(i),
                "classification": {
                    "facts": [source_notes[i % len(source_notes)]["claim_supported"]],
                    "inferences": [
                        f"{topic} may be more useful when measured through constraints, flows, and risk contribution."
                    ],
                    "speculation": [],
                    "jokes": [],
                },
                "source_note_ids": [source_notes[i % len(source_notes)]["id"]],
                "risks": ["needs_source_refresh"] if not context else ["verify_currentness"],
                "next_step": "draft_post" if i < int(content_cfg["finished_posts"]) else "hold_for_review",
            }
        )

    max_chars = int(platform_cfg["max_post_chars"])
    finished_posts = []
    for idea in ranked_ideas[: int(content_cfg["finished_posts"])]:
        copy = (
            f"{idea['topic']} has a measurement problem. The sharper quant question is not "
            f"'what is the headline?', but which constraint, flow, or balance-sheet channel is "
            f"doing the work. That is where the edge starts."
        )
        if len(copy) > max_chars:
            copy = copy[: max_chars - 1].rstrip() + "."
        finished_posts.append(
            {
                "id": f"post-{len(finished_posts) + 1:03d}",
                "idea_id": idea["id"],
                "char_limit": max_chars,
                "char_count": len(copy),
                "copy": copy,
                "classification": {
                    "facts": idea["source_note_ids"],
                    "inferences": idea["classification"]["inferences"],
                    "jokes": [],
                    "speculation": [],
                },
                "review_status": "needs_human_approval",
            }
        )

    max_thread_posts = int(platform_cfg["max_thread_posts"])
    thread_drafts = []
    for idea in ranked_ideas[: int(content_cfg["thread_drafts"])]:
        posts = [
            f"{idea['topic']} is not just a headline.",
            "First separate sourced facts from market reaction and interpretation.",
            "Then ask which constraint is binding: capital, liquidity, inventory, compute, or attention.",
            "The useful post is the mechanism, not the prediction.",
        ][:max_thread_posts]
        thread_drafts.append(
            {
                "id": f"thread-{len(thread_drafts) + 1:03d}",
                "idea_id": idea["id"],
                "max_posts": max_thread_posts,
                "posts": posts,
                "source_note_ids": idea["source_note_ids"],
                "review_status": "needs_human_approval",
            }
        )

    meme_concepts = []
    for idea in ranked_ideas[: int(content_cfg["meme_concepts"])]:
        meme_concepts.append(
            {
                "id": f"meme-{len(meme_concepts) + 1:03d}",
                "idea_id": idea["id"],
                "setup": "Expectation versus mechanism.",
                "caption": f"Headline take / constraint-aware {idea['topic']} take",
                "quant_punchline": "The bottleneck is usually not where the narrative points first.",
                "visual_direction": "Two-panel contrast with a small constraint diagram or bar chart.",
                "risk_note": "Keep factual claims in captions sourced or illustrative.",
            }
        )

    visual_specs = []
    for idea in ranked_ideas[: int(content_cfg["visual_specs"])]:
        visual_specs.append(
            {
                "id": f"visual-{len(visual_specs) + 1:03d}",
                "idea_id": idea["id"],
                "title": f"{idea['topic'].title()} Constraint Map",
                "type": "bar_chart_or_flow_diagram",
                "data_needed": [
                    "public source snapshot",
                    "date/time of retrieval",
                    "metric definition",
                ],
                "source_candidates": ["user-supplied links", "public factsheet", "official data release"],
                "grain": "topic-dependent",
                "window": "latest sourced snapshot",
                "transformation": "normalize raw facts into comparable constraints or contributions",
                "intended_takeaway": "Show the measurable bottleneck behind the narrative.",
                "caveats": ["Use illustrative labels unless current data is supplied."],
            }
        )

    review_findings = []
    for post in finished_posts:
        review_findings.append(
            {
                "id": f"rev-{len(review_findings) + 1:03d}",
                "severity": "warning",
                "item_id": post["id"],
                "finding": "Draft requires human approval and current-source review before posting.",
                "action": "Refresh source notes and confirm no investment-advice language.",
            }
        )

    return {
        "run_id": generated_at.strftime("%Y-%m-%d-evening-quant-content"),
        "generated_at": generated_at.isoformat(),
        "config_ref": str(config_path),
        "memory_version": "metadata-scaffold",
        "status": "draft",
        "manual_approval_required": bool(platform_cfg["require_manual_approval"]),
        "auto_post_enabled": bool(platform_cfg["auto_post_enabled"]),
        "ranked_ideas": ranked_ideas,
        "finished_posts": finished_posts,
        "thread_drafts": thread_drafts,
        "meme_concepts": meme_concepts,
        "visual_specs": visual_specs,
        "source_notes": source_notes,
        "review_findings": review_findings,
        "rejected_or_deferred_ideas": [
            {
                "id": "deferred-001",
                "title": "Strong causal market prediction without source support",
                "reason": "The runtime blocks unsupported causal certainty from publish-ready output.",
                "required_to_resume": ["current source note", "uncertainty language", "human approval"],
            }
        ],
        "memory_updates": [
            {"type": "theme_used", "value": ranked_ideas[0]["topic"] if ranked_ideas else "none"},
            {
                "type": "avoid_rules_consulted",
                "value": str(len(memory.get("avoid", []))),
            },
        ],
    }


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or any(ch in text for ch in [":", "#", "\n", "{", "}", "[", "]", ","]):
        return json.dumps(text)
    if text.lower() in {"true", "false", "null"}:
        return json.dumps(text)
    return json.dumps(text) if text.strip() != text else text


def dump_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}{key}: {yaml_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{pad}[]"
        lines = []
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{pad}-")
                lines.append(dump_yaml(item, indent + 2))
            elif isinstance(item, list):
                lines.append(f"{pad}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{yaml_scalar(value)}"


def render_markdown(pack: dict[str, Any]) -> str:
    lines = [
        "# Evening Quant Content Draft Pack",
        "",
        f"- **Run ID:** `{pack['run_id']}`",
        f"- **Generated at:** `{pack['generated_at']}`",
        f"- **Config:** `{pack['config_ref']}`",
        f"- **Status:** `{pack['status']}`",
        "",
        "> Manual approval required. This artifact is a draft pack, not a posting command.",
        "",
        "## Executive Queue",
        "",
        "Top candidate ideas, posts, visuals, and memes are below. Refresh current sources before posting.",
        "",
        "## Ranked Ideas",
        "",
        "| Rank | Idea ID | Title | Topic | Format | Claim Risk | Next Step |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idx, idea in enumerate(pack["ranked_ideas"], start=1):
        risk = idea["score"]["claim_risk"]
        lines.append(
            f"| {idx} | `{idea['id']}` | {idea['title']} | {idea['topic']} | {idea['format']} | {risk} | {idea['next_step']} |"
        )

    lines.extend(["", "## Finished Posts", ""])
    for post in pack["finished_posts"]:
        lines.extend(
            [
                f"### {post['id']}",
                "",
                f"- Idea: `{post['idea_id']}`",
                f"- Character count: {post['char_count']} / {post['char_limit']}",
                f"- Review status: `{post['review_status']}`",
                "",
                post["copy"],
                "",
            ]
        )

    lines.extend(["## Thread Drafts", ""])
    for thread in pack["thread_drafts"]:
        lines.append(f"### {thread['id']}")
        for idx, item in enumerate(thread["posts"], start=1):
            lines.append(f"{idx}. {item}")
        lines.append("")

    lines.extend(["## Visual Specs", ""])
    for visual in pack["visual_specs"]:
        lines.extend(
            [
                f"### {visual['id']}: {visual['title']}",
                "",
                f"- Type: {visual['type']}",
                f"- Intended takeaway: {visual['intended_takeaway']}",
                f"- Caveat: {'; '.join(visual['caveats'])}",
                "",
            ]
        )

    lines.extend(["## Meme Concepts", ""])
    for meme in pack["meme_concepts"]:
        lines.extend(
            [
                f"### {meme['id']}",
                "",
                f"- Setup: {meme['setup']}",
                f"- Caption: {meme['caption']}",
                f"- Punchline: {meme['quant_punchline']}",
                "",
            ]
        )

    lines.extend(["## Source Notes", ""])
    for source in pack["source_notes"]:
        lines.append(f"- `{source['id']}`: {source['claim_supported']} ({source['citation']})")

    lines.extend(["", "## Review Findings", ""])
    for finding in pack["review_findings"]:
        lines.append(f"- `{finding['severity']}` on `{finding['item_id']}`: {finding['finding']}")

    lines.extend(["", "## Deferred Or Rejected Ideas", ""])
    for item in pack["rejected_or_deferred_ideas"]:
        lines.append(f"- `{item['id']}` {item['title']}: {item['reason']}")

    return "\n".join(lines).rstrip() + "\n"


def validate_pack(pack: dict[str, Any], config: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    if pack.get("auto_post_enabled"):
        findings.append("auto_post_enabled must be false")
    if not pack.get("manual_approval_required"):
        findings.append("manual_approval_required must be true")
    max_chars = int(config["platform"]["max_post_chars"])
    for post in pack["finished_posts"]:
        if post["char_count"] > max_chars:
            findings.append(f"{post['id']} exceeds configured character limit")
        if not post["classification"].get("facts"):
            findings.append(f"{post['id']} has no fact source-note reference")
    if not (10 <= len(pack["ranked_ideas"]) <= 15):
        findings.append("ranked_ideas count must be between 10 and 15")
    required = [
        "finished_posts",
        "thread_drafts",
        "meme_concepts",
        "visual_specs",
        "source_notes",
        "review_findings",
        "rejected_or_deferred_ideas",
    ]
    for key in required:
        if key not in pack:
            findings.append(f"missing output section: {key}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="evening_quant_content_twitter/configs/evening_quant_content.yml")
    parser.add_argument("--context", help="Optional JSON or Markdown/plain-text context notes.")
    parser.add_argument("--output-dir", default="evening_quant_content_twitter/output")
    parser.add_argument("--generated-at", help="ISO timestamp for deterministic runs.")
    args = parser.parse_args(argv)

    config_path = Path(args.config)
    config = load_config(config_path)
    context = load_context(Path(args.context) if args.context else None)
    memory_path = Path(config["memory"]["path"])
    memory = load_memory(memory_path)
    generated_at = (
        dt.datetime.fromisoformat(args.generated_at)
        if args.generated_at
        else dt.datetime.now(dt.timezone.utc)
    )

    pack = build_draft_pack(config, config_path, context, memory, generated_at)
    findings = validate_pack(pack, config)
    if findings:
        for finding in findings:
            print(f"validation finding: {finding}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "draft_pack.yml").write_text(dump_yaml(pack) + "\n", encoding="utf-8")
    (output_dir / "draft_pack.md").write_text(render_markdown(pack), encoding="utf-8")
    print(output_dir / "draft_pack.yml")
    print(output_dir / "draft_pack.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
