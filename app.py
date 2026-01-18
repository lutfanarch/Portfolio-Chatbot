import json
from pathlib import Path

import streamlit as st

APP_TITLE = "Interactive Portfolio Bot"
APP_BUILD = "2026-01-18-privacy-no-certs-no-phone"
PROFILE_PATH = Path("profile.json")


# -------------------------
# Helpers
# -------------------------
def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_join_lines(lines) -> str:
    if not lines:
        return ""
    return "\n".join([f"- {x}" for x in lines])


def format_values(values: list) -> str:
    if not values:
        return ""
    out = []
    for v in values:
        value = (v.get("value") or "").strip() or "Value"
        evidence = (v.get("evidence") or "").strip()
        if evidence:
            out.append(f"- **{value}**: {evidence}")
        else:
            out.append(f"- **{value}**")
    return "\n".join(out).strip()


def format_growth_areas(items: list) -> str:
    if not items:
        return ""
    out = []
    for it in items:
        area = (it.get("area") or "").strip() or "Area"
        mitigation = (it.get("mitigation") or "").strip()
        if mitigation:
            out.append(f"- **{area}**: {mitigation}")
        else:
            out.append(f"- **{area}**")
    return "\n".join(out).strip()


def format_learning(learning_items: list) -> str:
    """Render learning without an Evidence block (repo links are shown in Repos & Links)."""
    if not learning_items:
        return "I haven't added learning items yet."

    out = []
    for item in learning_items:
        title = item.get("title", "Untitled")
        provider = item.get("provider", "Unknown provider")
        status = item.get("status", "Unknown status")
        what = item.get("what_i_learned", [])

        out.append(f"**{title}** ({provider}) — {status}")
        if what:
            out.append("What I learned:\n" + safe_join_lines(what))
        out.append("")

    return "\n".join(out).strip()


def format_projects(projects: list) -> str:
    if not projects:
        return "I haven't added projects yet."

    out = []
    for p in projects:
        name = p.get("name", "Untitled project")
        status = (p.get("status") or "").strip()
        summary = (p.get("summary") or "").strip()
        tech = p.get("tech", [])
        highlights = p.get("highlights", [])
        repo = (p.get("repo") or "").strip()
        demo = (p.get("demo") or "").strip()

        out.append(f"**{name}**")
        if status:
            out.append(f"Status: {status}")
        if summary:
            out.append(summary)

        if tech:
            out.append("")
            out.append("**Tech**")
            out.append(safe_join_lines(tech))

        if highlights:
            out.append("")
            out.append("**Highlights**")
            out.append(safe_join_lines(highlights))

        if repo:
            out.append("")
            out.append(f"Repo: {repo}")
        if demo:
            out.append(f"Demo: {demo}")

        out.append("\n---\n")

    return "\n".join(out).strip()


def format_repos_and_links(profile: dict) -> str:
    e = profile.get("evidence_and_links", {})
    links = profile.get("links", {}) if isinstance(profile.get("links", {}), dict) else {}

    github = e.get("github") or links.get("github")
    streamlit_demo = e.get("streamlit_demo") or links.get("streamlit_demo")
    project_repos = e.get("project_repos", [])

    parts = []
    if github:
        parts.append(f"GitHub: {github}")
    if streamlit_demo:
        parts.append(f"Streamlit demo: {streamlit_demo}")

    if isinstance(project_repos, list) and project_repos:
        parts.append("Projects:")
        lines = []
        for item in project_repos:
            if not isinstance(item, dict):
                continue
            project = item.get("project", "Project")
            repo = item.get("repo", "")
            demo = item.get("demo", "")
            if repo:
                lines.append(f"- {project}\n  - Repo: {repo}")
            else:
                lines.append(f"- {project}")
            if demo:
                lines.append(f"  - Demo: {demo}")
        if lines:
            parts.append("\n".join(lines).strip())

    return "\n\n".join(parts).strip() if parts else "No links added yet."


def answer_from_topic(profile: dict, topic_key: str) -> str:
    if topic_key == "about":
        about = profile.get("about", {})
        purpose = about.get("purpose_of_portfolio", [])
        bio = about.get("short_bio", [])
        values = about.get("values", [])
        growth = about.get("growth_areas", [])

        parts = []
        if purpose:
            parts.append("**Purpose of this portfolio**\n\n" + safe_join_lines(purpose))
        if bio:
            parts.append("**Introduction**\n\n" + safe_join_lines(bio))
        if values:
            parts.append("**Values**\n\n" + format_values(values))
        if growth:
            parts.append("**Growth areas**\n\n" + format_growth_areas(growth))

        return "\n\n".join([p for p in parts if p]).strip() or "I haven't filled in my About section yet."

    if topic_key == "academics":
        a = profile.get("academics", {})
        context = a.get("context", [])
        snapshot = a.get("elr2b2_snapshot", {})
        math_stmt = a.get("math_statement", {})

        parts = []
        if context:
            parts.append("**Context**\n\n" + safe_join_lines(context))

        if isinstance(snapshot, dict) and snapshot:
            rows = [f"- {k}: {v}" for k, v in snapshot.items()]
            parts.append("**Snapshot**\n\n" + "\n".join(rows))

        if isinstance(math_stmt, dict) and math_stmt:
            w = (math_stmt.get("what_happened") or "").strip()
            hv = (math_stmt.get("how_i_view_it") or "").strip()
            doing = math_stmt.get("what_i_am_doing_now", [])

            sub = []
            if w:
                sub.append(f"- What happened: {w}")
            if hv:
                sub.append(f"- How I view it: {hv}")
            if doing:
                sub.append("**What I'm doing now**\n" + safe_join_lines(doing))
            if sub:
                parts.append("**Math (statement)**\n\n" + "\n".join(sub))

        return "\n\n".join([p for p in parts if p]).strip() or "I haven't added academics details yet."

    if topic_key == "ns":
        ns = profile.get("ns", {})
        status = (ns.get("status") or "").strip()
        ord_date = (ns.get("ord_date") or "").strip()
        rank = (ns.get("rank") or "").strip()
        highlights = ns.get("highlights", [])

        parts = []
        if status or ord_date:
            line = []
            if status:
                line.append(f"Status: {status}")
            if ord_date:
                line.append(f"ORD: {ord_date}")
            parts.append("**National Service**\n\n- " + " | ".join(line))

        if rank:
            parts.append("**Rank**\n\n- " + rank)

        if highlights:
            parts.append("**Highlights**\n\n" + safe_join_lines(highlights))

        return "\n\n".join([p for p in parts if p]).strip() or "I haven't added my NS details yet."

    if topic_key == "why_ict_ai":
        why = profile.get("why_ict_ai", {})
        parts = []
        why_ict = why.get("why_ict", [])
        why_ai = why.get("why_ai", [])
        careers = why.get("career_interests", [])
        teamwork = why.get("teamwork", [])

        if why_ict:
            parts.append("**Why ICT**\n\n" + safe_join_lines(why_ict))
        if why_ai:
            parts.append("**Why AI**\n\n" + safe_join_lines(why_ai))
        if careers:
            parts.append("**Career interests**\n\n" + safe_join_lines(careers))
        if teamwork:
            parts.append("**Teamwork**\n\n" + safe_join_lines(teamwork))

        return "\n\n".join([p for p in parts if p]).strip() or "I haven't added my Why ICT/AI section yet."

    if topic_key == "learning":
        return format_learning(profile.get("learning", []))

    if topic_key == "projects":
        return format_projects(profile.get("projects", []))

    if topic_key == "skills":
        skills = profile.get("skills", {})
        tech = skills.get("technical", [])
        prof = skills.get("professional", [])
        parts = []
        if tech:
            parts.append("**Technical skills**\n\n" + safe_join_lines(tech))
        if prof:
            parts.append("**Professional skills**\n\n" + safe_join_lines(prof))
        return "\n\n".join([p for p in parts if p]).strip() or "I haven't added skills yet."

    if topic_key == "repos_links":
        return format_repos_and_links(profile)

    if topic_key == "contact":
        contact = profile.get("contact", {})
        email = contact.get("email") or profile.get("meta", {}).get("contact_email")
        preferred = (contact.get("preferred") or "Email").strip()
        notes = (contact.get("notes") or "").strip()

        if not email:
            return "I haven't added contact details yet."

        lines = [f"Preferred contact: {preferred}", f"Email: {email}"]
        if notes:
            lines.append(f"Notes: {notes}")
        return "\n".join(lines)

    return "I don't have that topic filled in yet."


def detect_topic(user_text: str) -> str | None:
    t = (user_text or "").strip().lower()
    if not t:
        return None

    mapping = {
        "about": ["about", "who are you", "introduce", "introduction", "bio", "purpose"],
        "academics": ["academic", "academics", "grades", "o level", "olevel", "elr2b2", "math", "emath"],
        "ns": ["ns", "national service", "army", "ord", "sergeant", "3sg"],
        "why_ict_ai": ["why", "ict", "ai", "computing", "infocomm", "motivation", "interest"],
        "learning": ["learning", "course", "codecademy", "practice"],
        "projects": ["project", "projects", "build", "built", "portfolio bot", "chatbot", "jarvis", "trader"],
        "skills": ["skill", "skills", "strengths", "tools"],
        "repos_links": ["repo", "repos", "repository", "repositories", "github", "links", "demo", "streamlit"],
        "contact": ["contact", "email", "reach", "message"],
    }

    for key, keywords in mapping.items():
        for kw in keywords:
            if kw in t:
                return key

    return None


# -------------------------
# App
# -------------------------
st.set_page_config(page_title=APP_TITLE, page_icon="📌", layout="centered")

try:
    profile = load_json(PROFILE_PATH)
except Exception as e:
    st.error(f"Could not load profile.json: {e}")
    st.stop()

meta = profile.get("meta", {})
display_name = meta.get("display_name", "Portfolio Owner")
tagline = meta.get("role_tagline", "")
disclaimer = meta.get("disclaimer", "")

st.title(APP_TITLE)
st.caption(f"{display_name} — {tagline}".strip(" —"))
if disclaimer:
    st.info(disclaimer)

st.sidebar.caption(f"Build: {APP_BUILD}")

page = st.sidebar.radio(
    "Pages",
    ["Chat", "Admissions View", "Repos & Links"],
    index=0,
)

quick_topics = [
    ("About", "about"),
    ("Academics", "academics"),
    ("National Service", "ns"),
    ("Why ICT / AI", "why_ict_ai"),
    ("Learning", "learning"),
    ("Projects", "projects"),
    ("Skills", "skills"),
    ("Repos & Links", "repos_links"),
    ("Contact", "contact"),
]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. I am an interactive portfolio bot.\n\n"
                "I answer strictly from profile.json (deterministic; no LLM).\n\n"
                "Topics you can ask:\n"
                "- About\n- Academics\n- National Service\n"
                "- Why ICT/AI\n- Learning\n- Projects\n- Skills\n"
                "- Repos & Links\n- Contact\n\n"
                "Tip: Use the 'Ask more' buttons at the bottom after each reply."
            ),
        }
    ]


def push_topic(label: str, key: str) -> None:
    text = answer_from_topic(profile, key)
    st.session_state.messages.append({"role": "user", "content": label})
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.rerun()


if page == "Chat":
    st.subheader("Quick Topics")
    with st.expander("Quick topics (optional)", expanded=False):
        cols = st.columns(3)
        for i, (label, key) in enumerate(quick_topics):
            with cols[i % 3]:
                if st.button(label, use_container_width=True, key=f"quick_{key}"):
                    push_topic(label, key)

    st.subheader("Chat")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.divider()
    st.subheader("Ask more")
    st.caption("Tap a button to continue without scrolling back up.")
    cols2 = st.columns(3)
    for i, (label, key) in enumerate(quick_topics):
        with cols2[i % 3]:
            if st.button(label, use_container_width=True, key=f"askmore_{key}"):
                push_topic(label, key)

    user_input = st.chat_input("Ask about a topic (e.g., Projects, Repos & Links)...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        topic = detect_topic(user_input)
        if topic is None:
            response = (
                "I can only answer using the data in profile.json.\n\n"
                "Try: About, Academics, National Service, Why ICT/AI, Learning, Projects, Skills, Repos & Links, Contact."
            )
        else:
            response = answer_from_topic(profile, topic)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

elif page == "Admissions View":
    st.subheader("Admissions View (Deterministic Summary)")

    st.markdown("### About")
    st.markdown(answer_from_topic(profile, "about"))

    st.markdown("### Academics")
    st.markdown(answer_from_topic(profile, "academics"))

    st.markdown("### National Service")
    st.markdown(answer_from_topic(profile, "ns"))

    st.markdown("### Why ICT / AI")
    st.markdown(answer_from_topic(profile, "why_ict_ai"))

    st.markdown("### Learning")
    st.markdown(answer_from_topic(profile, "learning"))

    st.markdown("### Projects")
    st.markdown(answer_from_topic(profile, "projects"))

    st.markdown("### Skills")
    st.markdown(answer_from_topic(profile, "skills"))

    st.markdown("### Repos & Links")
    st.markdown(answer_from_topic(profile, "repos_links"))

    st.markdown("### Contact")
    st.markdown(answer_from_topic(profile, "contact"))

else:
    st.subheader("Repos & Links")
    st.markdown(answer_from_topic(profile, "repos_links"))
