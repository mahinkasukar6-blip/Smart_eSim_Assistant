
import streamlit as st
import shutil
import subprocess
import importlib.util
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from tool_checker import TOOLS

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SMART eSIM 3.0 | Enterprise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ENTERPRISE CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f6fa;
    color: #172033;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #111c32;
    border-right: 1px solid #263650;
}

[data-testid="stSidebar"] * {
    color: #e5eaf3;
}

.hero {
    background: white;
    border: 1px solid #e1e6ef;
    border-radius: 14px;
    padding: 25px 30px;
    margin-bottom: 20px;
}

.hero-title {
    color: #14233d;
    font-size: 29px;
    font-weight: 800;
}

.hero-subtitle {
    color: #75839a;
    font-size: 13px;
    margin-top: 7px;
}

.section-title {
    color: #263a5b;
    font-size: 19px;
    font-weight: 700;
    margin: 18px 0;
}

.enterprise-card {
    background: white;
    border: 1px solid #e1e6ef;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    transition: 0.2s ease;
}

.enterprise-card:hover {
    border-color: #8ba9d4;
    box-shadow: 0 4px 15px rgba(30, 65, 110, 0.08);
}

.card-label {
    color: #75839a;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-value {
    color: #172d50;
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

.tool-card {
    background: white;
    border: 1px solid #e1e6ef;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
}

.tool-name {
    color: #172d50;
    font-size: 18px;
    font-weight: 700;
}

.tool-version {
    color: #75839a;
    font-size: 12px;
    margin-top: 8px;
}

.stButton > button {
    background: #2457a6;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #173e7c;
    color: white;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1e6ef;
    border-radius: 12px;
    padding: 16px;
}

div[data-testid="stMetricValue"] {
    color: #2457a6;
    font-weight: 800;
}

hr {
    border-color: #e1e6ef;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# TOOL SCANNER
# ==========================================

def get_tool_status():

    results = {}

    for name, details in TOOLS.items():

        command = details["command"]

        if shutil.which(command):

            try:
                result = subprocess.run(
                    details["version"],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                version = (
                    result.stdout.strip()
                    or result.stderr.strip()
                    or "Version unavailable"
                ).splitlines()[0]

                results[name] = {
                    "status": "Installed",
                    "version": version
                }

            except Exception:

                results[name] = {
                    "status": "Installed",
                    "version": "Version check failed"
                }

        else:

            results[name] = {
                "status": "Missing",
                "version": "Not available"
            }

    return results


# ==========================================
# SESSION STATE
# ==========================================

if "last_scan" not in st.session_state:
    st.session_state.last_scan = datetime.now()

if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "tool_status" not in st.session_state:
    st.session_state.tool_status = get_tool_status()
    st.session_state.scan_count += 1


def refresh_scanner():
    st.session_state.tool_status = get_tool_status()
    st.session_state.last_scan = datetime.now()
    st.session_state.scan_count += 1


status = st.session_state.tool_status

total = len(status)

installed = sum(
    1 for item in status.values()
    if item["status"] == "Installed"
)

missing = total - installed

health = round(installed / total * 100) if total else 0


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("""
<div style="padding:15px 5px 22px 5px;">
    <div style="font-size:32px;">⚡</div>
    <div style="font-size:23px;font-weight:800;">SMART eSIM</div>
    <div style="font-size:11px;color:#9eacc1;letter-spacing:1px;">
        ENTERPRISE CONTROL CENTER
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "Tool Monitor",
        "Dependencies",
        "Analytics",
        "Activity Logs"
    ]
)

st.sidebar.divider()

st.sidebar.caption("VERSION 3.0")
st.sidebar.caption("eSim Winter Internship 2026")

st.sidebar.markdown("---")

st.sidebar.metric("Tool Availability", f"{health}%")

if st.sidebar.button("Refresh System", use_container_width=True):
    refresh_scanner()
    st.rerun()


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-title">SMART eSIM 3.0</div>
    <div class="hero-subtitle">
        ENTERPRISE ELECTRONIC DESIGN AUTOMATION TOOL MANAGER
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Workspace: {page}  |  "
    f"Last scan: {st.session_state.last_scan.strftime('%d %b %Y, %I:%M:%S %p')}"
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "Total Tools", total),
        (c2, "Installed", installed),
        (c3, "Missing", missing),
        (c4, "Tool Availability", f"{health}%")
    ]

    for column, label, value in metrics:

        column.markdown(f"""
        <div class="enterprise-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.markdown("### Tool Availability")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=health,
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2457a6"},
                    "steps": [
                        {"range": [0, 50], "color": "#fce8e8"},
                        {"range": [50, 100], "color": "#e1edff"}
                    ]
                }
            )
        )

        gauge.update_layout(height=280)

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with right:

        st.markdown("### Installation Distribution")

        distribution = pd.DataFrame({
            "Status": ["Installed", "Missing"],
            "Count": [installed, missing]
        })

        donut = px.pie(
            distribution,
            names="Status",
            values="Count",
            hole=0.65,
            color="Status",
            color_discrete_map={
                "Installed": "#2457a6",
                "Missing": "#e36b6b"
            }
        )

        donut.update_layout(height=280)

        st.plotly_chart(
            donut,
            use_container_width=True
        )

    st.markdown("---")

    st.markdown("### Tool Status")

    for name, details in status.items():

        with st.container(border=True):

            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"**{name}**")
                st.caption(details["version"])

            with right:

                if details["status"] == "Installed":
                    st.success("Installed")
                else:
                    st.error("Missing")


# ==========================================
# TOOL MANAGEMENT CENTER
# ==========================================

elif page == "Tool Monitor":

    st.markdown("## Tool Management Center")

    search = st.text_input(
        "Search Tools",
        placeholder="Enter tool name..."
    )

    filter_status = st.selectbox(
        "Filter by Status",
        ["All", "Installed", "Missing"]
    )

    filtered_tools = {}

    for name, details in status.items():

        matches_search = search.lower() in name.lower()

        matches_status = (
            filter_status == "All"
            or details["status"] == filter_status
        )

        if matches_search and matches_status:
            filtered_tools[name] = details

    st.caption(f"Showing {len(filtered_tools)} of {total} tools")

    if filtered_tools:

        for name, details in filtered_tools.items():

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(f"### {name}")

                    st.caption(
                        f"Command: {TOOLS[name]['command']}"
                    )

                    st.caption(
                        f"Version: {details['version']}"
                    )

                with right:

                    if details["status"] == "Installed":
                        st.success("Installed")
                    else:
                        st.error("Missing")

    else:
        st.warning("No matching tools found.")

    st.markdown("---")

    st.markdown("### Installation Instructions")

    st.info(
        "To install a missing tool, use the existing command-line installer."
    )

    st.code("python tool_checker.py", language="bash")

    st.markdown("### Export Tool Report")

    report_data = []

    for name, details in status.items():

        report_data.append({
            "Tool": name,
            "Command": TOOLS[name]["command"],
            "Status": details["status"],
            "Version": details["version"]
        })

    report_df = pd.DataFrame(report_data)

    csv_data = report_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="smart_esim_tool_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==========================================
# DEPENDENCY CENTER
# ==========================================

elif page == "Dependencies":

    st.markdown("## Dependency Management")

    packages = [
        "logging",
        "subprocess",
        "shutil",
        "importlib",
        "streamlit",
        "plotly",
        "pandas"
    ]

    dependency_data = []

    for package in packages:

        if importlib.util.find_spec(package):
            dependency_data.append({
                "Package": package,
                "Status": "Available"
            })
        else:
            dependency_data.append({
                "Package": package,
                "Status": "Missing"
            })

    dependency_df = pd.DataFrame(dependency_data)

    available = sum(
        1 for item in dependency_data
        if item["Status"] == "Available"
    )

    percentage = round(
        available / len(packages) * 100
    )

    st.metric(
        "Dependency Availability",
        f"{percentage}%"
    )

    st.progress(percentage / 100)

    st.dataframe(
        dependency_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# ANALYTICS
# ==========================================

elif page == "Analytics":

    st.markdown("## System Analytics")

    chart_data = pd.DataFrame({
        "Tool": list(status.keys()),
        "Installed": [
            1 if item["status"] == "Installed" else 0
            for item in status.values()
        ]
    })

    chart_data["Status"] = chart_data["Installed"].map({
        1: "Installed",
        0: "Missing"
    })

    fig = px.bar(
        chart_data,
        x="Tool",
        y="Installed",
        color="Status",
        text="Status",
        color_discrete_map={
            "Installed": "#2457a6",
            "Missing": "#e36b6b"
        },
        title="Tool Installation Analysis"
    )

    fig.update_layout(
        height=400,
        yaxis={
            "tickmode": "array",
            "tickvals": [0, 1],
            "ticktext": ["Missing", "Installed"],
            "range": [0, 1.2]
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Summary")

    a, b, c = st.columns(3)

    a.metric("Total Tools", total)
    b.metric("Installed", installed)
    c.metric("Missing", missing)

    st.markdown("### Scan Statistics")

    st.metric(
        "Total Scans This Session",
        st.session_state.scan_count
    )


# ==========================================
# ACTIVITY CENTER
# ==========================================

elif page == "Activity Logs":

    st.markdown("## Activity Center")

    st.metric(
        "Total Scans This Session",
        st.session_state.scan_count
    )

    st.write(
        "Last scan:",
        st.session_state.last_scan.strftime(
            "%d %b %Y, %I:%M:%S %p"
        )
    )

    st.markdown("---")

    if os.path.exists("activity.log"):

        with open("activity.log", "r") as file:
            logs = file.read()

        if logs:

            st.text_area(
                "Activity History",
                logs,
                height=400
            )

        else:
            st.info("No activity recorded yet.")

    else:
        st.info("Activity log has not been created yet.")

    if st.button("Refresh Activity"):
        st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#75839a;
    font-size:12px;
    padding:15px;
">
    <b>SMART eSIM 3.0</b><br><br>
    ENTERPRISE CONTROL CENTER<br>
    PYTHON • STREAMLIT • PLOTLY
</div>
""", unsafe_allow_html=True)
