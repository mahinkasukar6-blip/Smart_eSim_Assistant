
import streamlit as st
import shutil
import subprocess
import importlib.util
import os
import logging

from tool_checker import TOOLS

# Page configuration
st.set_page_config(
    page_title="Smart eSim Assistant",
    page_icon="⚙️",
    layout="wide"
)

# Sidebar
st.sidebar.title("⚙️ Smart eSim")
st.sidebar.caption("Automated Tool Manager")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Tool Status", "Install Tools",
     "Dependencies", "Activity Logs"]
)

st.sidebar.divider()
st.sidebar.caption("eSim Winter Internship 2026")

# Tool detection
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

            except Exception:
                version = "Version check failed"

            results[name] = {
                "status": "Installed",
                "version": version
            }

        else:
            results[name] = {
                "status": "Missing",
                "version": "Not available"
            }

    return results


status = get_tool_status()

installed = sum(
    1 for item in status.values()
    if item["status"] == "Installed"
)

missing = len(TOOLS) - installed

# Dashboard
if page == "Dashboard":

    st.title("⚙️ Smart eSim Assistant")
    st.write("Welcome to your automated electronic design tool manager.")

    st.divider()

    st.subheader("📊 System Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tools", len(TOOLS))
    col2.metric("Installed Tools", installed)
    col3.metric("Missing Tools", missing)

    st.divider()

    st.subheader("🔧 Installed Tool Overview")

    for name, details in status.items():

        if details["status"] == "Installed":
            st.success(f"✅ {name} — Installed")
            st.caption(f"Version: {details['version']}")

        else:
            st.error(f"❌ {name} — Missing")

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

# Tool Status
elif page == "Tool Status":

    st.title("🔧 Tool Status")
    st.write("Check the installation status and versions of tools.")

    for name, details in status.items():

        if details["status"] == "Installed":
            st.success(f"✅ {name} — Installed")
            st.write(f"Version: {details['version']}")

        else:
            st.error(f"❌ {name} — Missing")

# Install Tools
elif page == "Install Tools":

    st.title("📥 Install Missing Tools")
    st.write("Use the command-line installer to install missing software.")

    if missing == 0:
        st.success("All required tools are already installed!")

    else:
        st.warning(f"{missing} tool(s) need attention.")

        for name, details in status.items():

            if details["status"] == "Missing":
                st.error(f"{name} is not installed.")

        st.info(
            "To install a missing tool, open Ubuntu terminal, "
            "activate your virtual environment, and run:"
        )

        st.code("python tool_checker.py", language="bash")

        st.caption(
            "The installer will ask you to select a tool and confirm "
            "before installing it."
        )

# Dependencies
elif page == "Dependencies":

    st.title("📦 Python Dependencies")

    packages = ["logging", "subprocess", "shutil", "importlib"]

    for package in packages:

        if importlib.util.find_spec(package):
            st.success(f"✅ {package} — Available")

        else:
            st.error(f"❌ {package} — Missing")

# Activity Logs
elif page == "Activity Logs":

    st.title("📋 Activity Logs")
    st.write("View recorded application activities.")

    if os.path.exists("activity.log"):

        with open("activity.log", "r") as file:
            logs = file.read()

        if logs:
            st.text_area(
                "Application Activity",
                logs,
                height=350
            )
        else:
            st.info("The activity log is empty.")

    else:
        st.info("No activity log found yet.")

# Footer
st.divider()

st.caption(
    "Smart eSim Assistant | Python + Streamlit | "
    "eSim Winter Internship 2026"
)
