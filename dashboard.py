
import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Data Deletion Assurance",
    page_icon="🛡️",
    layout="wide",
)

BASE = Path(__file__).resolve().parent

def load_records(filename):
    path = BASE / filename
    if not path.exists():
        return [], f"{filename} was not found."
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return [], f"{filename} must contain a JSON list."
        return data, None
    except (OSError, ValueError) as exc:
        return [], f"Unable to read {filename}: {exc}"

lineage, lineage_error = load_records("data_lineage.json")
audit, audit_error = load_records("audit_log.json")

checks = [
    x for x in audit
    if x.get("event_type") == "DELETION_VERIFICATION"
]

def result(event):
    fields = ("source_check", "vector_check", "lineage_check")
    if not event.get("data_id") or any(
        type(event.get(k)) is not bool for k in fields
    ):
        return "INCOMPLETE"
    if (
        event.get("status") == "PASS"
        and all(event[k] is True for k in fields)
    ):
        return "PASS"
    if (
        event.get("status") == "FAIL"
        or any(event[k] is False for k in fields)
    ):
        return "FAIL"
    return "INCOMPLETE"

st.markdown("""
<style>
.stApp {background: #FBFAFD;}
h1, h2, h3 {color: #51247A;}
.block-container {padding-top: 1.5rem; max-width: 1150px;}
.hero {
    background: #51247A;
    color: white;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 22px;
}
.hero h1 {color: white; margin: 0;}
.hero p {color: #E8DCF2; margin-bottom: 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Can We Prove Data Was Deleted?</h1>
  <p>AI Data Deletion Assurance · University of Queensland Capstone</p>
</div>
""", unsafe_allow_html=True)

pages = [
    "Introduction",
    "How Deletion Works",
    "Verification Results",
    "Governance & Cost",
]

page = st.radio(
    "Explore the project",
    pages,
    horizontal=True,
    label_visibility="collapsed",
)

if page == pages[0]:
    st.header("The story behind the project")

    video = BASE / "capstone video updated.mp4"
    if video.exists():
        st.video(str(video))
    else:
        st.info(
            "Place your 56-second video in this folder "
            "as 'capstone video.mp4'."
        )

    st.subheader("Why does this matter?")
    st.write(
        "Healthcare organisations increasingly use AI to work "
        "with information. But deleting an original document "
        "does not necessarily remove related information "
        "stored elsewhere in an AI system."
    )

    st.info(
        "Our goal: help organisations track information, "
        "check deletion outcomes, and keep evidence "
        "of what was done."
    )

    st.subheader("What did this project deliver?")
    a, b, c = st.columns(3)
    a.success("A governance framework")
    b.success("A local AI prototype")
    c.success("Recorded verification evidence")

    st.caption(
        "The framework is proposed for organisational use. "
        "The prototype demonstrates selected local controls."
    )


elif page == pages[1]:
    st.header("Explore the AI System")
    st.caption(
        "Select a component to understand how information "
        "is processed, deleted and verified."
    )

    components = {
        "📄 Source Documents": {
            "technology": "Local text files",
            "purpose": (
                "These are the original documents used "
                "by the AI application."
            ),
            "deletion": (
                "The targeted original file is removed "
                "from local storage."
            ),
            "verification": (
                "The system checks whether the targeted "
                "file still exists."
            ),
        },
        "🧠 Embeddings": {
            "technology": "all-MiniLM-L6-v2",
            "purpose": (
                "Documents are converted into numerical "
                "representations so relevant information "
                "can be searched."
            ),
            "deletion": (
                "Associated stored embeddings are removed "
                "from the vector database."
            ),
            "verification": (
                "The system checks for associated vector "
                "records in ChromaDB."
            ),
        },
        "🗄️ Vector Database": {
            "technology": "ChromaDB",
            "purpose": (
                "Stores embeddings and related information "
                "for retrieval."
            ),
            "deletion": (
                "Vector records associated with the "
                "targeted document are removed."
            ),
            "verification": (
                "The system checks whether associated "
                "records remain in the collection."
            ),
        },
        "🤖 Local LLM": {
            "technology": "Ollama · Gemma 3 1B",
            "purpose": (
                "Generates answers using the relevant "
                "context retrieved from the database."
            ),
            "deletion": (
                "The prototype does not perform "
                "model-weight unlearning."
            ),
            "verification": (
                "Model-weight deletion is outside "
                "the implemented verification scope."
            ),
        },
    }

    st.subheader("1. AI Data Processing Architecture")

    names = list(components.keys())
    cols = st.columns(4)

    for col, name in zip(cols, names):
        with col:
            st.markdown(f"**{name}**")
            st.caption(components[name]["technology"])

    selected = st.selectbox(
        "Select a component to explore",
        names,
        index=2,
    )

    component = components[selected]

    with st.container(border=True):
        st.subheader(selected)
        st.caption(component["technology"])

        st.markdown("**What does it do?**")
        st.write(component["purpose"])

        st.markdown("**What happens during deletion?**")
        st.write(component["deletion"])

        st.markdown("**How is it verified?**")
        st.write(component["verification"])

    st.divider()

    st.subheader("2. Deletion Assurance Workflow")

    workflow = [
        ("01", "Remove Source",
         "Delete the targeted original file."),
        ("02", "Purge Vectors",
         "Remove associated records from ChromaDB."),
        ("03", "Update Lineage",
         "Record the deletion status and metadata."),
        ("04", "Verify & Record",
         "Check the outcomes and save audit evidence."),
    ]

    cols = st.columns(4)

    for col, (number, title, description) in zip(cols, workflow):
        with col:
            with st.container(border=True):
                st.caption(f"STEP {number}")
                st.markdown(f"**{title}**")
                st.write(description)

    st.divider()

    st.subheader("3. Governance & Evidence")

    a, b, c = st.columns(3)

    with a:
        with st.container(border=True):
            st.markdown("**🔗 Data Lineage**")
            st.code("data_lineage.json")
            st.caption(
                "Tracks data origins, ownership "
                "and deletion status."
            )

    with b:
        with st.container(border=True):
            st.markdown("**📋 Audit Evidence**")
            st.code("audit_log.json")
            st.caption(
                "Stores historical verification "
                "outcomes."
            )

    with c:
        with st.container(border=True):
            st.markdown("**📊 Evidence Dashboard**")
            st.caption(
                "Displays recorded results "
                "for review."
            )

    with st.expander("🔍 Technical Verification Criteria"):
        st.markdown("""
        - **Source check:** Is the original file absent?
        - **Vector check:** Are associated records absent?
        - **Lineage check:** Is the deletion status recorded?

        A complete PASS requires all three checks.
        """)

    st.info(
        "This is an interactive explanation of the "
        "local prototype architecture. Selecting a component "
        "does not execute deletion or modify stored data."
    )

    st.caption(
        "Scope limitation: Backups, external services "
        "and model-weight unlearning are not verified."
    )

elif page == pages[2]:
    st.header("Did the deletion checks succeed?")
    st.write(
        "These results come from historical prototype audit "
        "records. The dashboard does not perform live deletion."
    )

    for err in (lineage_error, audit_error):
        if err:
            st.warning(err)

    passed = sum(result(x) == "PASS" for x in checks)
    failed = sum(result(x) == "FAIL" for x in checks)
    incomplete = sum(result(x) == "INCOMPLETE" for x in checks)

    a, b, c = st.columns(3)
    a.metric("✅ Complete PASS", passed)
    b.metric("❌ Failed checks", failed)
    c.metric("ℹ️ Incomplete records", incomplete)

    if checks:
        st.subheader("Explore a recorded verification")

        ordered = sorted(
            checks,
            key=lambda x: str(x.get("timestamp", "")),
            reverse=True,
        )

        selected = st.selectbox(
            "Choose an audit event",
            range(len(ordered)),
            format_func=lambda i: (
                f"{ordered[i].get('timestamp', 'Unknown date')} "
                f"· {ordered[i].get('data_id') or 'Unknown record'} "
                f"· {result(ordered[i])}"
            ),
        )

        event = ordered[selected]
        status = result(event)

        if status == "PASS":
            st.success(
                "All three recorded verification checks passed."
            )
        elif status == "FAIL":
            st.error(
                "Deletion could not be fully verified. "
                "At least one check failed."
            )
        else:
            st.warning(
                "There is insufficient evidence to establish "
                "a complete verification result."
            )

        labels = {
            "source_check": "Original document",
            "vector_check": "AI search database",
            "lineage_check": "Deletion record",
        }

        for field, label in labels.items():
            value = event.get(field)
            if value is True:
                st.write(f"✅ {label}: Check passed")
            elif value is False:
                st.write(f"❌ {label}: Check failed")
            else:
                st.write(f"ℹ️ {label}: Not recorded")

        with st.expander("View original audit evidence"):
            st.json(event)

        st.subheader("Historical verification events")
        rows = [
            {
                "Date": x.get("timestamp", "—"),
                "Data ID": x.get("data_id") or "—",
                "Result": result(x),
            }
            for x in ordered
        ]
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No recorded verification events were found.")

    st.caption(
        "PASS applies only to the three recorded checks. "
        "It does not establish deletion from backups, "
        "external services, logs or model weights."
    )

else:
    st.header("Governance and practical value")

    st.write(
        "The governance framework helps organisations "
        "identify AI-related information, assign responsibility, "
        "trace data movement, guide deletion and retain evidence."
    )

    st.subheader("The governance approach")
    for name in [
        "AI Discovery & Inventory",
        "Risk & Governance",
        "Data Lifecycle & Provenance",
        "Policy & Controls",
        "Deletion Assurance & Evidence",
    ]:
        st.write(f"✓ {name}")

    with st.expander("Future operational integration"):
        st.write(
            "Microsoft Purview integration, organisation-wide "
            "AI discovery and automated MLOps workflows "
            "are proposed future extensions."
        )

    st.divider()
    st.subheader("Could this approach reduce manual effort?")
    st.caption(
        "Illustrative cost model only — not measured Lifeblood data."
    )

    requests = st.select_slider(
        "Deletion requests per year",
        options=[1, 10, 50],
        value=10,
    )
    rate = st.number_input(
        "Illustrative staff cost (AUD/hour)",
        min_value=0,
        value=60,
    )
    manual_hours = st.number_input(
        "Manual hours per request",
        min_value=0.0,
        value=3.0,
        step=0.5,
    )
    guided_hours = st.number_input(
        "Framework-guided hours per request",
        min_value=0.0,
        value=1.0,
        step=0.5,
    )

    manual_cost = requests * rate * manual_hours
    guided_cost = requests * rate * guided_hours

    a, b, c = st.columns(3)
    a.metric("Manual labour", f"A${manual_cost:,.0f}")
    b.metric("Guided labour", f"A${guided_cost:,.0f}")
    c.metric(
        "Labour difference",
        f"A${manual_cost - guided_cost:,.0f}",
    )

    st.warning(
        "These are hypothetical labour estimates, not "
        "verified savings. Implementation, maintenance, "
        "infrastructure and licensing costs are excluded."
    )

st.divider()
st.caption(
    "Academic proof of concept · Read-only evidence viewer · "
    "Not connected to Lifeblood production systems or Microsoft Purview"
)
