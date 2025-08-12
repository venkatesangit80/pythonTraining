"""
Ticket Rule Mapper – Streamlit App
---------------------------------
A simple Streamlit UI that:
1) Accepts an Excel ticket dump (.xlsx)
2) Skips the first row (metadata) and uses the second row as headers
3) Lets you define rules:
   - Keyword Rule: if Column contains any of the given keywords → assign Category
   - Mapping Rule: if Column value equals one of the map keys → assign mapped Category
4) Applies rules in order (top to bottom) and writes the chosen output column
5) Allows downloading the updated Excel file

How to run:
  pip install -r requirements.txt   # or: pip install streamlit pandas openpyxl
  streamlit run app.py

Notes:
- Rules are stored in st.session_state so you can add many before applying.
- You can export/import rules as JSON.
"""

import io
import json
from typing import List, Dict, Any

import pandas as pd
import streamlit as st

# ----------------------------
# Helpers
# ----------------------------

def read_excel_skip_first_row(file) -> pd.DataFrame:
    """Read an Excel file, skip the first *row* (assumed metadata),
    and treat the next row as header by re-reading with header=0 after skipping.
    """
    # We read once to count columns, then re-read properly.
    # Easiest approach: read all with no header, drop first row, set next row as header.
    df_raw = pd.read_excel(file, header=None, engine="openpyxl")
    if df_raw.empty:
        return pd.DataFrame()
    if len(df_raw) == 1:
        # Only one row → after skipping, nothing remains
        return pd.DataFrame()
    # Drop the first row (index 0)
    df = df_raw.iloc[1:].reset_index(drop=True)
    # Use the (new) first row as header
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    # Ensure columns are strings
    df.columns = [str(c) for c in df.columns]
    return df

# Rule schemas (stored in session_state["rules"]) like:
# {
#   "type": "keyword",              # or "mapping"
#   "column": "Description",
#   "keywords": ["ASAP", "urgent"],
#   "category": "Safety"
# }
# OR
# {
#   "type": "mapping",
#   "column": "Resolution Type",
#   "map": {"Integration":"Integration", "PEP Connect":"Integration"},
# }


def ensure_state():
    if "rules" not in st.session_state:
        st.session_state["rules"] = []
    if "output_column" not in st.session_state:
        st.session_state["output_column"] = "MappedCategory"


def add_keyword_rule(col: str, keywords: List[str], category: str):
    st.session_state["rules"].append({
        "type": "keyword",
        "column": col,
        "keywords": [k for k in (kw.strip() for kw in keywords) if k],
        "category": category.strip()
    })


def add_mapping_rule(col: str, mapping: Dict[str, str]):
    # Drop empty keys
    clean_map = {str(k): str(v) for k, v in mapping.items() if str(k).strip() != ""}
    st.session_state["rules"].append({
        "type": "mapping",
        "column": col,
        "map": clean_map
    })


def apply_rules(df: pd.DataFrame, rules: List[Dict[str, Any]], output_col: str) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if output_col not in out.columns:
        out[output_col] = None

    # Apply rules in order; later rules overwrite earlier ones if they also match
    for rule in rules:
        rtype = rule.get("type")
        col = rule.get("column")
        if col not in out.columns:
            continue
        if rtype == "keyword":
            kws = rule.get("keywords", [])
            cat = rule.get("category", "")
            if not kws or not cat:
                continue
            # case-insensitive contains-any
            mask = out[col].astype(str).str.contains("|".join([pd.regex.escape(k) for k in kws]), case=False, na=False)
            out.loc[mask, output_col] = cat
        elif rtype == "mapping":
            mapping = rule.get("map", {})
            if not mapping:
                continue
            out[output_col] = out.apply(
                lambda row: mapping.get(str(row[col]), row[output_col]), axis=1
            )
    return out


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)
    return buf.read()


# ----------------------------
# UI
# ----------------------------

st.set_page_config(page_title="Ticket Rule Mapper", page_icon="🧩", layout="wide")
ensure_state()

st.title("🧩 Ticket Rule Mapper")
st.caption("Upload a ticket dump Excel, define rules, and download the mapped result.")

with st.expander("⚙️ Settings", expanded=False):
    st.session_state["output_column"] = st.text_input(
        "Output column name (where categories will be written)",
        st.session_state["output_column"],
        help="This column will be added/overwritten with rule results.")

uploaded = st.file_uploader("Upload Excel (.xlsx) – first row is skipped automatically", type=["xlsx"]) 

if uploaded is not None:
    try:
        df = read_excel_skip_first_row(uploaded)
    except Exception as e:
        st.error(f"Failed to read Excel: {e}")
        df = pd.DataFrame()

    if df.empty:
        st.warning("No data after skipping first row. Please check the file.")
    else:
        st.success(f"Loaded {len(df)} rows × {len(df.columns)} columns.")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("🧱 Build Rules")
        cols = list(df.columns)
        if not cols:
            st.stop()

        tab_kw, tab_map, tab_rules = st.tabs(["Keyword Rule", "Mapping Rule", "Current Rules"])

        with tab_kw:
            col_kw1, col_kw2 = st.columns([1,1])
            with col_kw1:
                kw_col = st.selectbox("Column to search keywords in", options=cols, key="kw_col")
            with col_kw2:
                kw_category = st.text_input("Assign this Category if any keyword matches", value="Safety", key="kw_cat")
            kw_list_text = st.text_area(
                "Keywords (comma-separated)",
                value="ASAP, urgent, high priority",
                help="Case-insensitive contains-any match."
            )
            if st.button("➕ Add Keyword Rule"):
                keywords = [s.strip() for s in kw_list_text.split(",")]
                if not any(keywords) or not kw_category.strip():
                    st.error("Please enter at least one keyword and a category.")
                else:
                    add_keyword_rule(kw_col, keywords, kw_category)
                    st.success("Keyword rule added.")

        with tab_map:
            map_col = st.selectbox("Column to map values from", options=cols, key="map_col")
            st.caption("Enter pairs of FROM value → TO category. Add rows as needed.")
            # Provide a small editable table for mapping
            sample = pd.DataFrame({"FROM_value": ["Integration", "PEP Connect", "PAC Data Power"],
                                   "TO_category": ["Integration", "Integration", "Data Power"]})
            edited = st.data_editor(sample, num_rows="dynamic", use_container_width=True, key="map_editor")
            if st.button("➕ Add Mapping Rule"):
                mapping = {str(row["FROM_value"]): str(row["TO_category"]) for _, row in edited.iterrows() if str(row["FROM_value"]).strip() != ""}
                if not mapping:
                    st.error("Please specify at least one mapping pair.")
                else:
                    add_mapping_rule(map_col, mapping)
                    st.success("Mapping rule added.")

        with tab_rules:
            st.write("Rules are applied top → bottom. Drag to reorder using the arrows.")
            if st.session_state["rules"]:
                # Show rules as JSON list and allow deletion/reordering
                for i, r in enumerate(st.session_state["rules"]):
                    with st.expander(f"Rule {i+1}: {r['type'].upper()} on '{r['column']}'", expanded=False):
                        st.code(json.dumps(r, indent=2))
                        c1, c2, c3 = st.columns([1,1,6])
                        if c1.button("⬆️ Up", key=f"up_{i}") and i > 0:
                            st.session_state["rules"][i-1], st.session_state["rules"][i] = st.session_state["rules"][i], st.session_state["rules"][i-1]
                            st.experimental_rerun()
                        if c2.button("⬇️ Down", key=f"down_{i}") and i < len(st.session_state["rules"]) - 1:
                            st.session_state["rules"][i+1], st.session_state["rules"][i] = st.session_state["rules"][i], st.session_state["rules"][i+1]
                            st.experimental_rerun()
                        if c3.button("🗑️ Delete", key=f"del_{i}"):
                            st.session_state["rules"].pop(i)
                            st.experimental_rerun()
            else:
                st.info("No rules yet. Add some in the tabs above.")

            st.markdown("---")
            col_j1, col_j2 = st.columns(2)
            with col_j1:
                if st.button("💾 Export Rules JSON"):
                    st.session_state["rules_json"] = json.dumps(st.session_state["rules"], indent=2)
                rules_json = st.text_area("Rules JSON", value=st.session_state.get("rules_json", ""), height=200)
            with col_j2:
                st.caption("Paste rules JSON here and click Import to load.")
                import_json = st.text_area("Import Rules JSON", value="", height=200)
                if st.button("📥 Import Rules"):
                    try:
                        st.session_state["rules"] = json.loads(import_json)
                        st.success("Rules imported.")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Failed to import JSON: {e}")

        st.markdown("---")
        st.subheader("🚀 Apply Rules")
        apply_clicked = st.button("Run & Preview")
        if apply_clicked:
            updated = apply_rules(df, st.session_state["rules"], st.session_state["output_column"]) 
            if updated.empty:
                st.warning("No data to show.")
            else:
                st.success("Rules applied.")
                st.dataframe(updated.head(50), use_container_width=True)
                excel_bytes = to_excel_bytes(updated)
                st.download_button(
                    label="⬇️ Download Updated Excel",
                    data=excel_bytes,
                    file_name="tickets_mapped.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
else:
    st.info("Upload an Excel file to begin.")
