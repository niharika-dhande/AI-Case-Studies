"""Generate the ai-case-studies repository from Sanity.

Sanity is the single source of truth. This script reads the published
case studies, engineering areas, experiments and automations with GROQ
and writes Markdown files. Never edit the generated files by hand:
edit the content in Sanity Studio and run the sync again.

Usage:
    python scripts/sync_from_sanity.py                      # read live from Sanity
    python scripts/sync_from_sanity.py --snapshot data.json # read a saved snapshot
"""

from __future__ import annotations

import argparse
import json
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ID = "ck8wyssm"
DATASET = "production"
API_VERSION = "v2024-01-01"
SITE_BASE = "https://promptatwork.com/ai-lab/work"

ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIRS = ["case-studies", "engineering-areas", "patterns", "experiments", "automations"]

# Area items that describe a tech stack rather than an engineering pattern.
STACK_ITEMS = {
    "Next.js + TypeScript",
    "FastAPI + React",
    "Headless CMS + Postgres",
    "Testing & CI/CD",
    "Google OAuth, Drive & Gmail",
    "Live streaming (SSE)",  # listed as "Streaming (SSE)" under Systems
}

QUERY = """{
  "areas": *[_type=="engineeringArea" && !(_id in path("drafts.**"))] | order(order asc){
    "slug": slug.current, title, order, description, items},
  "projects": *[_type=="project" && !(_id in path("drafts.**"))] | order(publishedAt asc){
    title, "slug": slug.current, category, summary, stats, tech,
    overview, problem, solution, workflow, architecture, challenges, results, learnings, futureScope,
    "areas": engineeringAreas[]->slug.current,
    "parts": parts[]->{_type, title, "slug": slug.current},
    "diagrams": diagrams[]{title, caption, kind, mermaid, analogy, concept,
      loopBackTo, loopLabel,
      "steps": steps[]{label, detail}, "pairs": pairs[]{concept, analogy}}},
  "experiments": *[_type=="experiment" && !(_id in path("drafts.**"))]{
    title, "slug": slug.current, "areas": engineeringAreas[]->slug.current},
  "automations": *[_type=="automation" && !(_id in path("drafts.**"))]{
    title, "slug": slug.current, "areas": engineeringAreas[]->slug.current}
}"""

SECTIONS = [
    ("overview", "Overview"),
    ("problem", "The problem"),
    ("solution", "The solution"),
    ("workflow", "How it works"),
    ("architecture", "Architecture"),
    ("challenges", "Challenges"),
    ("results", "Results"),
    ("learnings", "What I learned"),
    ("futureScope", "Future scope"),
]

FOOTER = (
    "\n---\n\n"
    "<sub>Generated from Sanity by `scripts/sync_from_sanity.py`. "
    "Edit the content in Sanity Studio, not in this file.</sub>\n"
)


def fetch_live() -> dict:
    url = (
        f"https://{PROJECT_ID}.apicdn.sanity.io/{API_VERSION}/data/query/{DATASET}?"
        + urllib.parse.urlencode({"query": QUERY})
    )
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)["result"]


def site_link(slug: str) -> str:
    return f"{SITE_BASE}/{slug}"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n" + FOOTER, encoding="utf-8")


def as_text(value) -> str:
    """Return plain text for a string field or a Portable Text array."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        paragraphs = []
        for block in value:
            if isinstance(block, dict) and block.get("_type") == "block":
                paragraphs.append("".join(c.get("text", "") for c in block.get("children", [])))
        return "\n\n".join(p for p in paragraphs if p).strip()
    return ""


def mermaid_label(text: str) -> str:
    return text.replace('"', "'")


def diagram_markdown(diagram: dict) -> list[str]:
    """Render a Sanity diagram: Mermaid as-is, step lists as a Mermaid flow, analogies as a table."""
    lines = [f"### {diagram.get('title') or 'Diagram'}", ""]
    if diagram.get("mermaid"):
        lines += ["```mermaid", diagram["mermaid"], "```", ""]
    elif diagram.get("steps"):
        flow = ["flowchart LR"]
        for i, step in enumerate(diagram["steps"]):
            label = mermaid_label(step.get("label") or f"Step {i + 1}")
            flow.append(f'  s{i}["{label}"]')
            if i:
                flow.append(f"  s{i - 1} --> s{i}")
        back = diagram.get("loopBackTo")
        if isinstance(back, int) and 0 <= back < len(diagram["steps"]):
            label = mermaid_label(diagram.get("loopLabel") or "repeat")
            flow.append(f'  s{len(diagram["steps"]) - 1} -.->|"{label}"| s{back}')
        lines += ["```mermaid", "\n".join(flow), "```", ""]
    elif diagram.get("pairs"):
        lines += [f"| {diagram.get('concept') or 'Concept'} | {diagram.get('analogy') or 'Analogy'} |", "|---|---|"]
        lines += [f"| {p.get('concept', '')} | {p.get('analogy', '')} |" for p in diagram["pairs"]]
        lines.append("")
    else:
        return []
    if diagram.get("caption"):
        lines += [f"*{diagram['caption']}*", ""]
    return lines


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def area_links(slugs: list[str], areas_by_slug: dict, prefix: str) -> str:
    return " · ".join(
        f"[{areas_by_slug[s]['title']}]({prefix}engineering-areas/{s}.md)"
        for s in slugs or []
        if s in areas_by_slug
    )


def build_case_study(project: dict, areas_by_slug: dict) -> str:
    lines = [f"# {project['title']}", "", f"**{project['category']}**", ""]
    lines += [f"> {project['summary']}", ""]
    if project.get("areas"):
        lines += [f"**Engineering areas:** {area_links(project['areas'], areas_by_slug, '../../')}", ""]
    if project.get("stats"):
        lines += ["## At a glance", "", bullet_list(project["stats"]), ""]

    for field, heading in SECTIONS:
        text = as_text(project.get(field))
        if text:
            lines += [f"## {heading}", "", text, ""]

    rendered = [part for d in project.get("diagrams") or [] for part in diagram_markdown(d)]
    if rendered:
        lines += ["## Diagrams", ""] + rendered

    if project.get("tech"):
        lines += ["## Tech stack", "", " · ".join(f"`{t}`" for t in project["tech"]), ""]

    groups = {"experiment": "Experiments", "automation": "Automations", "prompt": "Prompt patterns"}
    parts = project.get("parts") or []
    if parts:
        lines += ["## Related work", ""]
        for kind, label in groups.items():
            matching = [p for p in parts if p["_type"] == kind]
            if not matching:
                continue
            lines += [f"**{label}**", ""]
            for part in matching:
                if kind in ("experiment", "automation"):
                    lines.append(f"- [{part['title']}](../../{kind}s/README.md#{part['slug']})")
                else:
                    lines.append(f"- {part['title']}")
            lines.append("")

    lines += [f"Read the full case study on [Prompt at Work]({site_link(project['slug'])})."]
    return "\n".join(lines)


def build_area(area: dict, data: dict) -> str:
    slug = area["slug"]
    projects = [p for p in data["projects"] if slug in (p.get("areas") or [])]
    experiments = [e for e in data["experiments"] if slug in (e.get("areas") or [])]
    automations = [a for a in data["automations"] if slug in (a.get("areas") or [])]

    lines = [f"# {area['title']}", "", area["description"], "", "## Capabilities", "", bullet_list(area["items"]), ""]
    if projects:
        lines += ["## Case studies", ""]
        lines += [f"- [{p['title']}](../case-studies/{p['slug']}/README.md)" for p in projects]
        lines.append("")
    if experiments:
        lines += ["## Experiments", ""]
        lines += [f"- [{e['title']}](../experiments/README.md#{e['slug']})" for e in experiments]
        lines.append("")
    if automations:
        lines += ["## Automations", ""]
        lines += [f"- [{a['title']}](../automations/README.md#{a['slug']})" for a in automations]
        lines.append("")
    return "\n".join(lines)


def build_patterns_index(data: dict) -> str:
    lines = [
        "# Engineering patterns",
        "",
        "The reusable patterns behind the case studies, grouped by engineering area. "
        "Each one gets its own page (problem, how it works, when to use it, trade-offs "
        "and the projects that use it) once its pattern document is published in Sanity.",
        "",
    ]
    seen: set[str] = set()
    for area in data["areas"]:
        patterns = []
        for item in area["items"]:
            key = item.lower().replace("live ", "")
            if item in STACK_ITEMS or key in seen:
                continue
            seen.add(key)
            patterns.append(item)
        if not patterns:
            continue
        lines += [f"## {area['title']}", "", bullet_list(patterns), ""]
    return "\n".join(lines)


def build_index(kind: str, entries: list[dict], areas_by_slug: dict) -> str:
    title = "Experiments" if kind == "experiments" else "Automations"
    intro = (
        "Controlled comparisons run while building the case studies."
        if kind == "experiments"
        else "Pipelines that turn manual, repeatable work into automated flows."
    )
    lines = [f"# {title}", "", intro, ""]
    for entry in entries:
        lines += [
            f'<a id="{entry["slug"]}"></a>',
            f"### {entry['title']}",
            "",
            f"Areas: {area_links(entry.get('areas'), areas_by_slug, '../')}",
            "",
        ]
    return "\n".join(lines)


def build_root(data: dict) -> str:
    lines = [
        "# AI Case Studies · Prompt at Work",
        "",
        "Engineering case studies by **Niharika Dhande**, AI Solutions Engineer: multi-agent systems, "
        "RAG pipelines, AI automation and the engineering patterns underneath them. "
        "Each case study covers the problem, the design decisions and their trade-offs, the architecture "
        "and what I learned.",
        "",
        f"Full write-ups: [promptatwork.com]({SITE_BASE}) · "
        "[LinkedIn](https://www.linkedin.com/in/niharikasaxenadhande)",
        "",
        "## Case studies",
        "",
        "| Case study | Category |",
        "|---|---|",
    ]
    for p in data["projects"]:
        lines.append(f"| [{p['title']}](case-studies/{p['slug']}/README.md) | {p['category']} |")
    lines += ["", "## Engineering areas", "", "| Area | Case studies | Experiments | Automations |", "|---|---|---|---|"]
    for area in data["areas"]:
        s = area["slug"]
        count = lambda rows: sum(1 for r in rows if s in (r.get("areas") or []))
        lines.append(
            f"| [{area['title']}](engineering-areas/{s}.md) | {count(data['projects'])} | "
            f"{count(data['experiments'])} | {count(data['automations'])} |"
        )
    lines += [
        "",
        "## More",
        "",
        "- [Engineering patterns](patterns/README.md)",
        f"- [Experiments](experiments/README.md) ({len(data['experiments'])})",
        f"- [Automations](automations/README.md) ({len(data['automations'])})",
        "",
        "## How this repository is built",
        "",
        "The content lives in Sanity CMS, the same source that powers promptatwork.com. "
        "A GitHub Action runs `scripts/sync_from_sanity.py`, which reads the published content "
        "with GROQ and regenerates these Markdown files, so the site and this repository never drift apart. "
        "Client names, credentials, endpoints and configuration are never included.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, help="read a saved JSON snapshot instead of Sanity")
    args = parser.parse_args()

    data = json.loads(args.snapshot.read_text(encoding="utf-8")) if args.snapshot else fetch_live()
    data["areas"].sort(key=lambda a: a.get("order", 999))
    areas_by_slug = {a["slug"]: a for a in data["areas"]}

    for name in GENERATED_DIRS:
        shutil.rmtree(ROOT / name, ignore_errors=True)

    write(ROOT / "README.md", build_root(data))
    for project in data["projects"]:
        write(ROOT / "case-studies" / project["slug"] / "README.md", build_case_study(project, areas_by_slug))
    write(ROOT / "engineering-areas" / "README.md",
          "# Engineering areas\n\n" + "\n".join(
              f"- [{a['title']}]({a['slug']}.md)" for a in data["areas"]))
    for area in data["areas"]:
        write(ROOT / "engineering-areas" / f"{area['slug']}.md", build_area(area, data))
    write(ROOT / "patterns" / "README.md", build_patterns_index(data))
    write(ROOT / "experiments" / "README.md", build_index("experiments", data["experiments"], areas_by_slug))
    write(ROOT / "automations" / "README.md", build_index("automations", data["automations"], areas_by_slug))
    print(f"Generated {len(data['projects'])} case studies and {len(data['areas'])} areas.")


if __name__ == "__main__":
    main()
