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

        # Display unique domains table
        df_unique = pd.DataFrame(unique_domains, columns=["Unique Domains"])
        st.dataframe(df_unique)

        # Display all domains (including duplicates) in text block
        all_domains_text = '\n'.join(domains)
        st.markdown("### 📋 Copy All Domains (with Duplicates) to Clipboard")
        st.code(all_domains_text, language="text")

        # HTML/JS Copy to Clipboard
        st.markdown("""
        <button onclick="navigator.clipboard.writeText(document.getElementById('to_copy').innerText)" 
            style="margin-top: 10px; padding: 8px 16px; font-size: 16px; border-radius: 6px; border: none; 
            background-color: #4CAF50; color: white; cursor: pointer;">
            📋 Copy to Clipboard
        </button>
        <pre id="to_copy" style="display:none;">{}</pre>
        """.format(all_domains_text), unsafe_allow_html=True)

        # Create Excel with two sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_unique.to_excel(writer, index=False, sheet_name='Unique Domains')
            pd.DataFrame(domains, columns=["All Domains (With Duplicates)"]).to_excel(writer, index=False, sheet_name='All Domains')
            writer.save()

        st.download_button(
            label="📥 Download Domains (Excel with 2 Sheets)",
            data=output.getvalue(),
            file_name="email_domains.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
