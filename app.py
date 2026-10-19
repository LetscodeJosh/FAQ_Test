from pathlib import Path
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# Page Configuration (Must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Troubleshooting Guide | Laptop Mouse FAQ",
    page_icon="🖱️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Structured FAQ Data (Category: Laptop Mouse)
# ---------------------------------------------------------------------------
FAQ_CATEGORY = "Laptop Mouse"

FAQ_ISSUES = [
    {
        "id": "mouse-not-connecting",
        "number": 1,
        "title": "Mouse is not connecting (Bluetooth or USB)",
        "tags": ["Bluetooth", "USB Receiver"],
        "steps": [
            {
                "num": 1,
                "conn": "both",
                "text": "Verify the power switch under the mouse is turned **ON**.",
                "hint": 'Flip the mouse over and check for a slider switch showing green or "ON".',
            },
            {
                "num": 2,
                "conn": "usb",
                "text": "**For USB:** Unplug the wireless receiver and plug it directly into a different USB port on your laptop.",
                "hint": "Avoid unpowered external USB hubs or adapters while testing connectivity.",
            },
            {
                "num": 3,
                "conn": "bluetooth",
                "text": "**For Bluetooth:** Open your laptop's Bluetooth settings, remove/forget the mouse, and re-pair the device.",
                "hint": "Hold the pairing button on the bottom of your mouse until its LED blinks rapidly to enter pairing mode.",
            },
            {
                "num": 4,
                "conn": "both",
                "text": "Replace the battery or connect the charging cable to ensure it has power.",
                "hint": "Low battery voltage can prevent wireless handshakes even if the sensor light briefly flickers.",
            },
        ],
    },
    {
        "id": "cursor-freezing-or-lagging",
        "number": 2,
        "title": "Cursor is freezing or lagging",
        "tags": ["Optical Sensor & Signal"],
        "steps": [
            {
                "num": 1,
                "conn": "both",
                "text": "Gently clean the optical sensor on the bottom of the mouse using a dry microfiber cloth or cotton swab.",
                "hint": "Even a tiny hair or dust speck over the lens can cause erratic cursor jumping or freezing.",
            },
            {
                "num": 2,
                "conn": "both",
                "text": "Test the mouse on a different surface or use a proper mousepad (avoid glass or highly reflective surfaces).",
                "hint": "Optical sensors require microscopic surface texture to track movement accurately.",
            },
            {
                "num": 3,
                "conn": "both",
                "text": "Move the mouse closer to the receiver to eliminate wireless interference.",
                "hint": "Keep metal objects, USB 3.0 hard drives, and Wi-Fi routers away from the line of sight between mouse and laptop.",
            },
            {
                "num": 4,
                "conn": "both",
                "text": "Restart your laptop to clear any temporary driver glitches.",
                "hint": "Re-initializes the operating system's HID (Human Interface Device) driver stack.",
            },
        ],
    },
    {
        "id": "scroll-wheel-is-not-responding",
        "number": 3,
        "title": "Scroll wheel is not responding",
        "tags": ["Wheel & OS Settings"],
        "steps": [
            {
                "num": 1,
                "conn": "both",
                "text": "Use compressed air to blow out any dust or debris trapped in the crevices around the scroll wheel.",
                "hint": "Dust inside the rotary encoder or optical wheel sensor commonly blocks scroll detection.",
            },
            {
                "num": 2,
                "conn": "both",
                "text": 'Open your laptop\'s Mouse Settings and verify the "Choose how many lines to scroll each time" slider is set greater than zero.',
                "hint": "In Windows: Settings > Bluetooth & devices > Mouse > Lines to scroll at a time (default is 3).",
            },
            {
                "num": 3,
                "conn": "both",
                "text": "Disconnect and reconnect the mouse to reset the connection.",
                "hint": "Toggle the mouse power switch off/on or re-insert the USB receiver to refresh scroll wheel reporting.",
            },
        ],
    },
    {
        "id": "battery-is-draining-too-fast",
        "number": 4,
        "title": "Battery is draining too fast",
        "tags": ["Power & Battery Life"],
        "steps": [
            {
                "num": 1,
                "conn": "both",
                "text": "Manually switch the mouse off when packing it away or not using it for long periods.",
                "hint": "When inside a laptop bag, slight movements constantly wake the optical sensor and drain the battery.",
            },
            {
                "num": 2,
                "conn": "both",
                "text": "If your mouse has RGB lighting, use the manufacturer's software to turn the lights off.",
                "hint": "Continuous LED illumination can consume up to 70% of a wireless mouse's total battery capacity.",
            },
            {
                "num": 3,
                "conn": "both",
                "text": "Replace alkaline batteries with fresh, high-quality name brands, or ensure your rechargeable mouse is plugged directly into the wall adapter rather than a low-power USB hub.",
                "hint": "Direct USB ports or wall chargers guarantee a full charge cycle for lithium-ion rechargeable mice.",
            },
        ],
    },
]


def load_bundled_html() -> str | None:
    """
    Reads index.html, styles.css, and script.js from the project directory
    and bundles them into a single self-contained HTML string for Streamlit.
    """
    base_dir = Path(__file__).parent
    index_path = base_dir / "index.html"
    css_path = base_dir / "styles.css"
    js_path = base_dir / "script.js"

    if not index_path.exists():
        return None

    html_content = index_path.read_text(encoding="utf-8")

    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        html_content = html_content.replace(
            '<link rel="stylesheet" href="styles.css" />',
            f"<style>\n{css_content}\n</style>",
        )

    if js_path.exists():
        js_content = js_path.read_text(encoding="utf-8")
        html_content = html_content.replace(
            '<script src="script.js"></script>',
            f"<script>\n{js_content}\n</script>",
        )

    return html_content


def init_session_state() -> None:
    if "checked_steps" not in st.session_state:
        st.session_state.checked_steps = {}
    if "resolved_issues" not in st.session_state:
        st.session_state.resolved_issues = {}
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = {issue["id"]: 0 for issue in FAQ_ISSUES}


def render_native_streamlit_mode() -> None:
    """Renders the FAQ & Troubleshooting Guide using native Streamlit widgets."""
    init_session_state()

    st.markdown(
        """
        <style>
        .faq-anchor-box {
            background: rgba(37, 99, 235, 0.08);
            border: 1px solid rgba(37, 99, 235, 0.25);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 20px;
        }
        .faq-anchor-box a {
            text-decoration: none;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Top Header Bar
    col_title, col_reset = st.columns([4, 1])
    with col_title:
        st.caption("Support Center / Hardware & Peripherals / **Category: Laptop Mouse**")
        st.title("🖱️ Laptop Mouse Troubleshooting Guide")
        st.write(
            "Encountering an issue with your laptop mouse? Select your symptom below or search keywords "
            "to jump straight to step-by-step instructions to troubleshoot your device in the meantime."
        )
    with col_reset:
        st.write("")
        st.write("")
        if st.button("↺ Reset Progress", use_container_width=True):
            st.session_state.checked_steps = {}
            st.session_state.resolved_issues = {}
            st.session_state.wizard_step = {issue["id"]: 0 for issue in FAQ_ISSUES}
            st.rerun()

    # Quick Issue Selector (Anchor Links matching user's format)
    with st.container(border=True):
        st.subheader(f"Category: {FAQ_CATEGORY}")
        st.markdown(
            """
- [Mouse is not connecting (Bluetooth or USB)](#mouse-not-connecting)
- [Cursor is freezing or lagging](#cursor-freezing-or-lagging)
- [Scroll wheel is not responding](#scroll-wheel-is-not-responding)
- [Battery is draining too fast](#battery-is-draining-too-fast)
            """
        )

    # Toolbar: Search & View Mode
    col_search, col_mode = st.columns([3, 1])
    with col_search:
        search_query = st.text_input(
            "Search symptoms or steps",
            placeholder="Search e.g. Bluetooth, USB, sensor, scroll, battery...",
            label_visibility="collapsed",
        ).strip().lower()
    with col_mode:
        guide_mode = st.segmented_control(
            "Guide Mode",
            options=["Full Guide", "Guided Mode"],
            default="Full Guide",
            label_visibility="collapsed",
        )

    # Overall Progress Calculation
    total_steps = sum(len(issue["steps"]) for issue in FAQ_ISSUES)
    completed_steps = sum(1 for v in st.session_state.checked_steps.values() if v)
    st.progress(
        completed_steps / total_steps if total_steps else 0,
        text=f"**Step by Step Instructions** — {completed_steps} of {total_steps} total troubleshooting steps tried",
    )

    # Filter issues by search query
    filtered_issues = []
    for issue in FAQ_ISSUES:
        haystack = (
            issue["title"]
            + " "
            + " ".join(s["text"] + " " + s["hint"] for s in issue["steps"])
        ).lower()
        if not search_query or search_query in haystack:
            filtered_issues.append(issue)

    if not filtered_issues:
        st.warning("No matching troubleshooting steps found. Try another keyword.")
        return

    # Guided Mode vs Full Guide Mode
    if guide_mode == "Guided Mode":
        selected_title = st.selectbox(
            "Select the issue you want to troubleshoot step-by-step:",
            options=[i["title"] for i in filtered_issues],
        )
        active_issues = [i for i in filtered_issues if i["title"] == selected_title]
    else:
        active_issues = filtered_issues

    for issue in active_issues:
        issue_id = issue["id"]
        steps = issue["steps"]
        done_count = sum(
            1
            for s in steps
            if st.session_state.checked_steps.get(f"{issue_id}-{s['num']}", False)
        )
        is_resolved = st.session_state.resolved_issues.get(issue_id, False)

        with st.container(border=True):
            # HTML Anchor for direct jumping
            st.markdown(f'<div id="{issue_id}"></div>', unsafe_allow_html=True)

            h_col1, h_col2 = st.columns([3, 1])
            with h_col1:
                status_badge = " ✅ **Resolved**" if is_resolved else ""
                st.subheader(f"{issue['number']}. {issue['title']}{status_badge}")
                st.caption(" • ".join(issue["tags"]))
            with h_col2:
                st.metric("Progress", f"{done_count} / {len(steps)} steps")

            # Optional connection filter for Issue #1
            conn_filter = "all"
            if issue_id == "mouse-not-connecting" and guide_mode != "Guided Mode":
                conn_choice = st.radio(
                    "Filter by connection type:",
                    options=["All (Bluetooth & USB)", "USB Receiver Only", "Bluetooth Only"],
                    horizontal=True,
                    key=f"conn_{issue_id}",
                )
                if conn_choice == "USB Receiver Only":
                    conn_filter = "usb"
                elif conn_choice == "Bluetooth Only":
                    conn_filter = "bluetooth"

            visible_steps = [
                s
                for s in steps
                if conn_filter == "all" or s["conn"] in ("both", conn_filter)
            ]

            if guide_mode == "Guided Mode":
                idx = st.session_state.wizard_step.get(issue_id, 0)
                idx = max(0, min(idx, len(visible_steps) - 1))
                current_step = visible_steps[idx]
                step_key = f"{issue_id}-{current_step['num']}"

                st.info(f"**Step {idx + 1} of {len(visible_steps)}**")
                checked = st.checkbox(
                    f"**Step {current_step['num']}:** {current_step['text']}",
                    value=st.session_state.checked_steps.get(step_key, False),
                    key=f"cb_wiz_{step_key}",
                )
                st.session_state.checked_steps[step_key] = checked
                st.caption(f"💡 *Tip: {current_step['hint']}*")

                w_col1, w_col2, w_col3 = st.columns([1, 2, 1])
                with w_col1:
                    if st.button("← Previous Step", key=f"prev_{issue_id}", disabled=(idx == 0)):
                        st.session_state.wizard_step[issue_id] = idx - 1
                        st.rerun()
                with w_col3:
                    if idx < len(visible_steps) - 1:
                        if st.button("Next Step →", key=f"next_{issue_id}", type="primary"):
                            st.session_state.checked_steps[step_key] = True
                            st.session_state.wizard_step[issue_id] = idx + 1
                            st.rerun()
            else:
                for s in visible_steps:
                    step_key = f"{issue_id}-{s['num']}"
                    checked = st.checkbox(
                        f"**{s['num']}.** {s['text']}",
                        value=st.session_state.checked_steps.get(step_key, False),
                        key=f"cb_{step_key}",
                    )
                    st.session_state.checked_steps[step_key] = checked
                    st.caption(f"   ↳ *{s['hint']}*")

            st.divider()
            f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
            with f_col1:
                st.write("**Did these steps resolve your issue?**")
            with f_col2:
                if st.button("✓ Yes, it's working!", key=f"yes_{issue_id}", use_container_width=True):
                    st.session_state.resolved_issues[issue_id] = True
                    st.toast("Glad your laptop mouse issue is resolved!", icon="✅")
                    st.rerun()
            with f_col3:
                if st.button("✕ Still not working", key=f"no_{issue_id}", use_container_width=True):
                    st.session_state.resolved_issues[issue_id] = False
                    st.session_state.escalate_issue = issue["title"]

    # Diagnostic Summary Generator
    with st.expander("📋 Still experiencing issues? Generate Troubleshooting Diagnostic Report", expanded=bool(st.session_state.get("escalate_issue"))):
        primary_symptom = st.selectbox(
            "Primary Symptom:",
            options=[i["title"] for i in FAQ_ISSUES],
            index=[i["title"] for i in FAQ_ISSUES].index(
                st.session_state.get("escalate_issue", FAQ_ISSUES[0]["title"])
            ),
        )
        report_lines = [
            "=== DEVICE TROUBLESHOOTING SUMMARY ===",
            f"Category: {FAQ_CATEGORY}",
            f"Primary Symptom: {primary_symptom}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "Completed Self-Service Steps:",
        ]
        any_checked = False
        for issue in FAQ_ISSUES:
            issue_checked = []
            for s in issue["steps"]:
                if st.session_state.checked_steps.get(f"{issue['id']}-{s['num']}", False):
                    clean_text = s["text"].replace("**", "")
                    issue_checked.append(f"  [x] Step {s['num']}: {clean_text}")
            if issue_checked:
                any_checked = True
                report_lines.append(f"\n• {issue['title']}:")
                report_lines.extend(issue_checked)

        if not any_checked:
            report_lines.append("  (No steps checked off yet in the interactive guide)")

        report_lines.append(
            "\nStatus: Issue persists after self-service troubleshooting. Requesting further assistance."
        )
        report_text = "\n".join(report_lines)
        st.code(report_text, language="text")
        st.download_button(
            "⬇ Download Diagnostic Report (.txt)",
            data=report_text,
            file_name="laptop_mouse_diagnostic_report.txt",
            mime="text/plain",
        )


def main() -> None:
    with st.sidebar:
        st.header("⚙️ Display Mode")
        display_mode = st.radio(
            "Choose how to view the FAQ project:",
            options=[
                "Interactive Web App (HTML/CSS/JS)",
                "Native Streamlit Widgets",
            ],
            index=0,
            help="Interactive Web App embeds the full custom HTML/CSS/JS website including the Live Mouse & Scroll Wheel Tester. Native Streamlit Widgets uses standard Streamlit components.",
        )
        st.divider()
        st.caption(
            "**Category: Laptop Mouse**\n"
            "Ready for deployment on [streamlit.io](https://streamlit.io)."
        )

    bundled_html = load_bundled_html()

    if display_mode == "Interactive Web App (HTML/CSS/JS)" and bundled_html:
        # Remove default Streamlit padding so the embedded website fills the viewport cleanly
        st.markdown(
            """
            <style>
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 0rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                max-width: 100% !important;
            }
            iframe {
                border: none !important;
                border-radius: 12px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        components.html(bundled_html, height=2400, scrolling=True)
    else:
        render_native_streamlit_mode()


if __name__ == "__main__":
    main()
