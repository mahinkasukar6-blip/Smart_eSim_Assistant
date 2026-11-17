
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

LOG_FILE = "activity.log"


# ==========================================
# ENTERPRISE DESIGN
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

.enterprise-card {
    background: white;
    border: 1px solid #e1e6ef;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
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
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
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
# ACTIVITY LOGGER
# ==========================================

def log_activity(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def read_activity():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        return file.readlines()


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
# DEPENDENCY SCANNER
# ==========================================

def get_dependency_status():

    packages = [
        "logging",
        "subprocess",
        "shutil",
        "importlib",
        "streamlit",
        "plotly",
        "pandas"
    ]

    results = {}

    for package in packages:

        try:
            available = importlib.util.find_spec(package) is not None
        except (ImportError, ValueError, ModuleNotFoundError):
            available = False

        results[package] = {
            "status": "Available" if available else "Missing"
        }

    return results


# ==========================================
# SYSTEM REPORT
# ==========================================

def create_system_report(tool_status, dependency_status):

    rows = []

    for name, details in tool_status.items():

        rows.append({
            "Category": "EDA Tool",
            "Component": name,
            "Status": details["status"],
            "Details": details["version"]
        })

    for name, details in dependency_status.items():

        rows.append({
            "Category": "Python Dependency",
            "Component": name,
            "Status": details["status"],
            "Details": "Python module/package availability"
        })

    return pd.DataFrame(rows)


# ==========================================
# SESSION STATE
# ==========================================

if "tool_status" not in st.session_state:

    st.session_state.tool_status = get_tool_status()

    installed_count = sum(
        1 for item in st.session_state.tool_status.values()
        if item["status"] == "Installed"
    )

    missing_count = (
        len(st.session_state.tool_status) - installed_count
    )

    log_activity(
        f"System scan completed | Installed: {installed_count} | Missing: {missing_count}"
    )

    st.session_state.scan_count = 1

else:

    if "scan_count" not in st.session_state:
        st.session_state.scan_count = 1


def refresh_scanner():

    st.session_state.tool_status = get_tool_status()

    installed_count = sum(
        1 for item in st.session_state.tool_status.values()
        if item["status"] == "Installed"
    )

    missing_count = (
        len(st.session_state.tool_status) - installed_count
    )

    st.session_state.scan_count += 1

    log_activity(
        f"System scan completed | Installed: {installed_count} | Missing: {missing_count}"
    )


# Get latest scan results

status = st.session_state.tool_status
dependency_status = get_dependency_status()

total = len(status)

installed = sum(
    1 for item in status.values()
    if item["status"] == "Installed"
)

missing = total - installed

health = round(installed / total * 100) if total else 0

dependency_total = len(dependency_status)

dependency_available = sum(
    1 for item in dependency_status.values()
    if item["status"] == "Available"
)

dependency_missing = dependency_total - dependency_available

dependency_health = (
    round(dependency_available / dependency_total * 100)
    if dependency_total else 0
)

combined_total = total + dependency_total
combined_available = installed + dependency_available

system_readiness = (
    round(combined_available / combined_total * 100)
    if combined_total else 0
)


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
        "Installation Readiness",
        "Analytics",
        "Activity Logs"
    ]
)

st.sidebar.divider()

st.sidebar.caption("VERSION 3.0")
st.sidebar.caption("eSim Winter Internship 2026")

st.sidebar.markdown("---")

st.sidebar.metric(
    "System Readiness",
    f"{system_readiness}%"
)

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
    f"Workspace: {page} | "
    f"Scans this session: {st.session_state.scan_count}"
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown("## System Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "Total Tools", total),
        (c2, "Installed", installed),
        (c3, "Missing", missing),
        (c4, "System Readiness", f"{system_readiness}%")
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

        st.plotly_chart(gauge, use_container_width=True)

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

        st.plotly_chart(donut, use_container_width=True)

    st.markdown("---")

    st.markdown("### Overall System Readiness")

    st.metric(
        "Combined Tool and Dependency Availability",
        f"{system_readiness}%"
    )

    st.progress(system_readiness / 100)

    st.caption(
        f"{combined_available} of {combined_total} "
        "components are available."
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
# TOOL MANAGEMENT
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
                    st.caption(f"Command: {TOOLS[name]['command']}")
                    st.caption(f"Version: {details['version']}")

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
        "Use the existing command-line installer to install missing tools. "
        "The dashboard does not install software directly."
    )

    st.code("python main.py", language="bash")

    st.caption(
        "Open your project terminal, activate your virtual environment, "
        "and select the tool installation option in the CLI menu."
    )

    st.markdown("### Export Tool Report")

    report_df = pd.DataFrame([
        {
            "Tool": name,
            "Command": TOOLS[name]["command"],
            "Status": details["status"],
            "Version": details["version"]
        }
        for name, details in status.items()
    ])

    csv_data = report_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV Report",
        data=csv_data,
        file_name="smart_esim_tool_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==========================================
# DEPENDENCIES
# ==========================================

elif page == "Dependencies":

    st.markdown("## Dependency Management")

    st.metric(
        "Dependency Availability",
        f"{dependency_health}%"
    )

    st.progress(dependency_health / 100)

    st.caption(
        f"{dependency_available} available | "
        f"{dependency_missing} missing"
    )

    dependency_df = pd.DataFrame([
        {
            "Package": name,
            "Status": details["status"]
        }
        for name, details in dependency_status.items()
    ])

    st.dataframe(
        dependency_df,
        use_container_width=True,
        hide_index=True
    )

    missing_packages = [
        name for name, details in dependency_status.items()
        if details["status"] == "Missing"
        and name in ["streamlit", "plotly", "pandas"]
    ]

    if missing_packages:

        st.warning("Some required third-party packages are missing.")

        install_command = (
            "python -m pip install " + " ".join(missing_packages)
        )

        st.code(install_command, language="bash")

    else:
        st.success("All checked dependencies are available.")


# ==========================================
# INSTALLATION READINESS
# ==========================================

elif page == "Installation Readiness":

    st.markdown("## Installation Readiness Center")

    st.caption(
        "Review the availability of EDA tools and Python dependencies."
    )

    r1, r2, r3 = st.columns(3)

    r1.metric("System Readiness", f"{system_readiness}%")
    r2.metric("Available Components", combined_available)
    r3.metric("Missing Components", combined_total - combined_available)

    st.progress(system_readiness / 100)

    if combined_available == combined_total:
        st.success("All checked tools and dependencies are available.")

    elif system_readiness >= 50:
        st.warning(
            "Some components are missing. Review the details below."
        )

    else:
        st.error(
            "System readiness is low. Several components need attention."
        )

    st.markdown("---")

    st.markdown("### EDA Tool Readiness")

    for name, details in status.items():

        with st.container(border=True):

            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"**{name}**")
                st.caption(details["version"])

            with right:

                if details["status"] == "Installed":
                    st.success("Ready")
                else:
                    st.error("Needs installation")

    missing_tools = [
        name for name, details in status.items()
        if details["status"] == "Missing"
    ]

    if missing_tools:

        st.markdown("### Missing EDA Tools")

        st.warning(
            "The following tools were not detected by the scanner:"
        )

        for name in missing_tools:
            st.write(f"- {name}")

        st.info(
            "To install missing tools, use the existing command-line "
            "installer from your project folder."
        )

        st.code("python main.py", language="bash")

    else:
        st.success("No missing EDA tools detected.")

    st.markdown("---")

    st.markdown("### Python Dependency Readiness")

    dependency_df = pd.DataFrame([
        {
            "Dependency": name,
            "Status": details["status"]
        }
        for name, details in dependency_status.items()
    ])

    st.dataframe(
        dependency_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.markdown("### Download Complete System Report")

    system_report = create_system_report(
        status,
        dependency_status
    )

    csv_data = system_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download System Readiness Report",
        data=csv_data,
        file_name="smart_esim_system_readiness_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "The report contains the latest tool scan and dependency check."
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

    st.plotly_chart(fig, use_container_width=True)

    a, b, c = st.columns(3)

    a.metric("Total Tools", total)
    b.metric("Installed", installed)
    c.metric("Missing", missing)

    st.markdown("---")

    st.markdown("### Dependency Analytics")

    dependency_chart = pd.DataFrame({
        "Status": ["Available", "Missing"],
        "Count": [dependency_available, dependency_missing]
    })

    dependency_fig = px.bar(
        dependency_chart,
        x="Status",
        y="Count",
        color="Status",
        color_discrete_map={
            "Available": "#2457a6",
            "Missing": "#e36b6b"
        },
        title="Python Dependency Analysis"
    )

    st.plotly_chart(
        dependency_fig,
        use_container_width=True
    )


# ==========================================
# ACTIVITY CENTER
# ==========================================

elif page == "Activity Logs":

    st.markdown("## System Activity Center")

    logs = read_activity()

    st.metric("Total Recorded Activities", len(logs))

    st.markdown("---")

    if logs:

        st.markdown("### Recent Activity Timeline")

        for entry in reversed(logs[-20:]):

            entry = entry.strip()

            if entry:
                with st.container(border=True):
                    st.write("🕒", entry)

        st.markdown("---")

        st.markdown("### Complete Activity History")

        st.text_area(
            "Activity Log",
            "".join(logs),
            height=300
        )

        st.download_button(
            "Download Activity Log",
            data="".join(logs),
            file_name="smart_esim_activity.log",
            mime="text/plain"
        )

    else:
        st.info("No activity recorded yet.")

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
