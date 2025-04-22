import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Email Domain Extractor", layout="wide")

st.title("📧 Email Domain Extractor")
st.markdown("Paste up to **1 million emails** (one per line) and click **Extract Domains** to get only the domains.")

emails_input = st.text_area("Paste your email list here:", height=300, help="Each email on a new line.")

if st.button("🚀 Extract Domains"):
    if not emails_input.strip():
        st.warning("Please paste some emails to extract.")
    else:
        emails = emails_input.strip().splitlines()
        emails = emails[:1_000_000]  # Limit to 1 million

        domains = [email.split('@')[1].strip() for email in emails if '@' in email]
        unique_domains = sorted(set(domains))

        st.success(f"✅ Extracted {len(domains)} domains ({len(unique_domains)} unique).")

        # Show Unique Domains (scrollable, like you want)
        st.markdown("### ✅ Unique Domains")
        df_unique = pd.DataFrame(unique_domains, columns=["Unique Domains"])
        st.dataframe(df_unique, height=300)

        # Show All Domains with duplicates (also scrollable now)
        st.markdown("### 📋 All Domains (With Duplicates)")
        df_all = pd.DataFrame(domains, columns=["All Domains"])
        st.dataframe(df_all, height=300)

        # Excel export: both sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_unique.to_excel(writer, index=False, sheet_name='Unique Domains')
            df_all.to_excel(writer, index=False, sheet_name='All Domains')
            writer.save()

        st.download_button(
            label="📥 Download Domains (Excel with 2 Sheets)",
            data=output.getvalue(),
            file_name="email_domains.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
