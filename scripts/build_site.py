#!/usr/bin/env python3
"""Build the public portfolio and machine-readable profile from one JSON source."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "profile.json"
TEMPLATE_PATH = ROOT / "site-src" / "index.html"
SITE_DIR = ROOT / "site"
PUBLIC_BASE = "https://subway-jack.github.io/resume/"
PHONE_RE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
REQUIRED_PRIVACY_EXCLUSIONS = {
    "government identifiers",
    "phone number",
    "private repositories",
    "street address",
    "third-party personal information",
}


class BuildError(RuntimeError):
    pass


def load_profile() -> dict[str, Any]:
    try:
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildError("profile_json_invalid") from exc
    if not isinstance(profile, dict) or profile.get("visibility") != "public":
        raise BuildError("profile_must_be_public")
    for key in ("person", "education", "publications", "projects", "privacy"):
        if key not in profile:
            raise BuildError(f"profile_missing_{key}")
    serialized = json.dumps(profile, ensure_ascii=False)
    if PHONE_RE.search(serialized):
        raise BuildError("public_profile_contains_phone_number")
    privacy_exclusions = set(profile.get("privacy", {}).get("excluded", []))
    if not REQUIRED_PRIVACY_EXCLUSIONS.issubset(privacy_exclusions):
        raise BuildError("public_profile_privacy_policy_incomplete")
    return profile


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def external_link(url: str, label: str, class_name: str = "text-link") -> str:
    if not url.startswith("https://"):
        raise BuildError("public_link_must_use_https")
    return (
        f'<a class="{esc(class_name)}" href="{esc(url)}" '
        f'target="_blank" rel="noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'
    )


def render_publications(profile: dict[str, Any]) -> str:
    items = []
    for index, publication in enumerate(profile["publications"], start=1):
        if not publication.get("evidence"):
            raise BuildError("publication_missing_evidence")
        links = "".join(
            external_link(url, label.title(), "evidence-link")
            for label, url in publication.get("links", {}).items()
        )
        highlights = "".join(
            f"<li>{esc(item)}</li>" for item in publication.get("highlights", [])
        )
        items.append(
            f"""
            <article class="evidence-item publication-item">
              <div class="evidence-index">0{index}</div>
              <div class="evidence-main">
                <div class="evidence-kicker"><span>{esc(publication['venue'])}</span><span>{esc(publication['year'])}</span></div>
                <h3>{esc(publication['title'])}</h3>
                <p class="evidence-role">{esc(publication['role'])}</p>
                <p>{esc(publication['summary'])}</p>
                <ul class="metric-list">{highlights}</ul>
                <div class="evidence-links">{links}</div>
              </div>
            </article>
            """
        )
    return "".join(items)


def render_projects(profile: dict[str, Any]) -> str:
    items = []
    for project in profile["projects"]:
        if not project.get("evidence"):
            raise BuildError("project_missing_evidence")
        technologies = "".join(
            f"<li>{esc(item)}</li>" for item in project.get("technologies", [])
        )
        highlights = "".join(
            f"<li>{esc(item)}</li>" for item in project.get("highlights", [])
        )
        items.append(
            f"""
            <article class="project-item">
              <div class="project-meta"><span>{esc(project['role'])}</span><span>{esc(project['year'])}</span></div>
              <h3>{external_link(project['url'], project['name'], 'project-title')}</h3>
              <p>{esc(project['summary'])}</p>
              {f'<ul class="project-highlights">{highlights}</ul>' if highlights else ''}
              <ul class="tech-list">{technologies}</ul>
            </article>
            """
        )
    return "".join(items)


def render_contributions(profile: dict[str, Any]) -> str:
    rows = []
    for contribution in profile.get("contributions", []):
        if not contribution.get("evidence"):
            raise BuildError("contribution_missing_evidence")
        rows.append(
            f"""
            <div class="contribution-row">
              <strong>{esc(contribution['project'])}</strong>
              <span>{esc(contribution['summary'])}</span>
              <span class="status-mark">{esc(contribution['status'])}</span>
              {external_link(contribution['url'], 'PR', 'compact-link')}
            </div>
            """
        )
    return "".join(rows)


def render_education(profile: dict[str, Any]) -> str:
    rows = []
    for item in profile["education"]:
        rows.append(
            f"""
            <article class="timeline-row">
              <div class="timeline-date">{esc(item['start'])}<br>{esc(item['end'])}</div>
              <div>
                <h3>{esc(item['institution'])}</h3>
                <p>{esc(item['degree'])}</p>
                <span>{esc(item['unit'])}</span>
              </div>
            </article>
            """
        )
    return "".join(rows)


def render_awards(profile: dict[str, Any]) -> str:
    return "".join(
        f"""
        <div class="award-row">
          <span>{esc(item['year'])}</span>
          <strong>{esc(item['title'])}</strong>
          <p>{esc(item['awarder'])}</p>
        </div>
        """
        for item in profile.get("awards", [])
    )


def render_focus(profile: dict[str, Any]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in profile.get("focus", []))


def json_ld(profile: dict[str, Any]) -> str:
    person = profile["person"]
    payload = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": person["name"],
        "alternateName": person.get("name_zh"),
        "url": person["website"],
        "image": f"{PUBLIC_BASE}assets/bowei-xia.jpg",
        "email": f"mailto:{person['email']}",
        "sameAs": [person["github"]],
        "alumniOf": [
            {
                "@type": "CollegeOrUniversity",
                "name": item["institution"],
            }
            for item in profile["education"]
        ],
        "knowsAbout": profile.get("focus", []),
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def normalize_generated_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def render_index(profile: dict[str, Any]) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    person = profile["person"]
    replacements = {
        "@@NAME@@": esc(person["name"]),
        "@@NAME_ZH@@": esc(person.get("name_zh", "")),
        "@@HEADLINE@@": esc(person["headline"]),
        "@@SUMMARY@@": esc(person["summary"]),
        "@@EMAIL@@": esc(person["email"]),
        "@@GITHUB@@": esc(person["github"]),
        "@@LAST_VERIFIED@@": esc(profile["last_verified"]),
        "@@FOCUS@@": render_focus(profile),
        "@@PUBLICATIONS@@": render_publications(profile),
        "@@PROJECTS@@": render_projects(profile),
        "@@CONTRIBUTIONS@@": render_contributions(profile),
        "@@EDUCATION@@": render_education(profile),
        "@@AWARDS@@": render_awards(profile),
        "@@JSON_LD@@": json_ld(profile),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    unresolved = sorted(set(re.findall(r"@@[A-Z_]+@@", template)))
    if unresolved:
        raise BuildError("unresolved_template_markers")
    return normalize_generated_text(template)


def render_resume_markdown(profile: dict[str, Any]) -> str:
    person = profile["person"]
    lines = [
        f"# {person['name']} ({person.get('name_zh', '')})",
        "",
        person["headline"],
        "",
        f"- Email: {person['email']}",
        f"- GitHub: {person['github']}",
        f"- Website: {person['website']}",
        "",
        "## Education",
        "",
    ]
    for item in profile["education"]:
        lines.append(
            f"- **{item['institution']}** — {item['degree']}, {item['start']} to {item['end']}"
        )
    lines.extend(["", "## Publications", ""])
    for item in profile["publications"]:
        lines.extend(
            [
                f"### {item['title']}",
                f"{item['role']} · {item['venue']} ({item['year']})",
                "",
                item["summary"],
                "",
                *[f"- {highlight}" for highlight in item.get("highlights", [])],
                *[f"- {label.title()}: {url}" for label, url in item.get("links", {}).items()],
                "",
            ]
        )
    lines.extend(["## Selected Projects", ""])
    for item in profile["projects"]:
        lines.extend(
            [
                f"### [{item['name']}]({item['url']})",
                f"{item['role']} · {item['year']}",
                "",
                item["summary"],
                "",
                *[f"- {highlight}" for highlight in item.get("highlights", [])],
                "",
            ]
        )
    lines.extend(["## Public Contributions", ""])
    for item in profile.get("contributions", []):
        lines.append(f"- [{item['project']}]({item['url']}): {item['summary']} ({item['status']})")
    lines.extend(["", f"Last verified: {profile['last_verified']}", ""])
    return "\n".join(lines)


def render_llms(profile: dict[str, Any]) -> str:
    person = profile["person"]
    publication_lines = "\n".join(
        f"- {item['title']} — {item['venue']} {item['year']} — {item['links']['paper']}"
        for item in profile["publications"]
    )
    project_lines = "\n".join(
        f"- {item['name']}: {item['summary']} — {item['url']}"
        for item in profile["projects"]
    )
    return f"""# {person['name']}

> {person['headline']}

Canonical structured profile: {PUBLIC_BASE}profile.json
Plain-text resume: {PUBLIC_BASE}resume.md
Human-readable PDF: {PUBLIC_BASE}bowei-xia-resume.pdf
GitHub: {person['github']}

## Research

{publication_lines}

## Selected open-source work

{project_lines}

## Usage boundary

Use only the evidence-backed public fields in profile.json. Do not infer private employment, contact details beyond the listed email, or third-party personal information.

Last verified: {profile['last_verified']}
"""


def agent_profile(profile: dict[str, Any]) -> dict[str, Any]:
    person = profile["person"]
    return {
        "schema_version": 1,
        "type": "public_person_profile",
        "name": person["name"],
        "canonical_url": PUBLIC_BASE,
        "profile": f"{PUBLIC_BASE}profile.json",
        "resume_markdown": f"{PUBLIC_BASE}resume.md",
        "resume_pdf": f"{PUBLIC_BASE}bowei-xia-resume.pdf",
        "llms_txt": f"{PUBLIC_BASE}llms.txt",
        "last_verified": profile["last_verified"],
        "usage_policy": profile["privacy"]["policy"],
    }


def expected_outputs(profile: dict[str, Any]) -> dict[Path, bytes]:
    pretty_profile = json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    outputs = {
        SITE_DIR / "index.html": render_index(profile).encode("utf-8"),
        SITE_DIR / "profile.json": pretty_profile.encode("utf-8"),
        SITE_DIR / "resume.md": render_resume_markdown(profile).encode("utf-8"),
        SITE_DIR / "llms.txt": render_llms(profile).encode("utf-8"),
        SITE_DIR / ".well-known" / "agent-profile.json": (
            json.dumps(agent_profile(profile), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8"),
        SITE_DIR / "robots.txt": (
            f"User-agent: *\nAllow: /\nSitemap: {PUBLIC_BASE}sitemap.xml\n"
        ).encode("utf-8"),
        SITE_DIR / "sitemap.xml": (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"  <url><loc>{PUBLIC_BASE}</loc></url>\n"
            f"  <url><loc>{PUBLIC_BASE}resume.md</loc></url>\n"
            f"  <url><loc>{PUBLIC_BASE}profile.json</loc></url>\n"
            "</urlset>\n"
        ).encode("utf-8"),
    }
    for asset_name in ("site.css", "site.js", "bowei-xia.jpg", "bowei-xia.webp"):
        outputs[SITE_DIR / "assets" / asset_name] = (
            ROOT / "site-src" / "assets" / asset_name
        ).read_bytes()
    source_pdf = ROOT / "resume-src" / "bowei-xia-resume.pdf"
    if source_pdf.exists():
        outputs[SITE_DIR / "bowei-xia-resume.pdf"] = source_pdf.read_bytes()
    return outputs


def check_outputs(outputs: dict[Path, bytes]) -> list[str]:
    stale = []
    for path, expected in outputs.items():
        try:
            actual = path.read_bytes()
        except OSError:
            stale.append(str(path.relative_to(ROOT)))
            continue
        if actual != expected:
            stale.append(str(path.relative_to(ROOT)))
    return stale


def write_outputs(outputs: dict[Path, bytes]) -> None:
    for path, payload in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated outputs are stale")
    args = parser.parse_args()
    try:
        profile = load_profile()
        outputs = expected_outputs(profile)
        if args.check:
            stale = check_outputs(outputs)
            if stale:
                print(json.dumps({"ok": False, "stale": stale}, sort_keys=True), file=sys.stderr)
                return 1
            print(json.dumps({"ok": True, "checked": len(outputs)}, sort_keys=True))
            return 0
        write_outputs(outputs)
    except (BuildError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "generated": len(outputs)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
