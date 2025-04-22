import streamlit as st
import pandas as pd

st.set_page_config(page_title="Email Domain Extractor", layout="wide")

st.title("📧 Email Domain Extractor")
st.markdown("Paste up to **1 million emails** (one per line) and click **Extract Domains** to get only the domains.")

# Text area to paste email list
emails_input = st.text_area("Paste your email list here:", height=300, help="Each email on a new line.")

if st.button("🚀 Extract Domains"):
    if not emails_input.strip():
        st.warning("Please paste some emails to extract.")
    else:
        emails = emails_input.strip().splitlines()
        # Limit to 1 million
        emails = emails[:1_000_000]

        domains = [email.split('@')[1].strip() for email in emails if '@' in email]
        df = pd.DataFrame(domains, columns=["Domain"])

        st.success(f"✅ Extracted {len(domains)} domains.")
        st.dataframe(df)

        # Convert to CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, file_name="extracted_domains.csv", mime="text/csv")

        # Display as text block for copying
        all_domains_text = '\n'.join(domains)
        st.markdown("### 📋 Copy Domains to Clipboard")
        st.code(all_domains_text, language="text")

        # Add a manual HTML copy button
        st.markdown("""
        <button onclick="navigator.clipboard.writeText(document.getElementById('to_copy').innerText)" style="margin-top: 10px; padding: 8px 16px; font-size: 16px; border-radius: 6px; border: none; background-color: #4CAF50; color: white; cursor: pointer;">📋 Copy to Clipboard</button>
        <pre id="to_copy" style="display:none;">{}</pre>
        """.format(all_domains_text), unsafe_allow_html=True)
