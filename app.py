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
        # Process input
        emails = emails_input.strip().splitlines()
        emails = emails[:1_000_000]  # Limit to 1 million

        # Check if first line is a header
        first_line = emails[0].strip().lower()
        if first_line in ["email", "email address", "emailaddress"]:
            emails = emails[1:]  # skip the header

        # Extract domains
        domains = [email.split('@')[1].strip() for email in emails if '@' in email]
        unique_domains = sorted(set(domains))

        # Display counts
        total_count = len(domains)
        unique_count = len(unique_domains)

        st.success(f"✅ Extracted {total_count} domains ({unique_count} unique).")

        # Create the tables
        df_unique = pd.DataFrame(unique_domains, columns=["Unique Domains"])
        df_all = pd.DataFrame(domains, columns=["All Domains"])

        # Unique Domains search with highlighting in yellow
        st.markdown(f"### ✅ Unique Domains - {unique_count}")
        search_input = st.text_input("Search Unique Domains", help="Search within unique domains.")
        
        if search_input:
            # Highlight matches in yellow
            df_unique['Highlighted Domains'] = df_unique['Unique Domains'].apply(
                lambda x: f'<span style="background-color: yellow">{x}</span>' if search_input.lower() in x.lower() else x
            )
            st.markdown(f"### ✅ Unique Domains - {unique_count}")
            st.write(df_unique.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.dataframe(df_unique, height=300)

        # All Domains (With Duplicates) search with highlighting in yellow
        st.markdown(f"### 📋 All Domains (With Duplicates) - {total_count}")
        search_input_all = st.text_input("Search All Domains", help="Search within all domains.")
        
        if search_input_all:
            # Highlight matches in yellow
            df_all['Highlighted Domains'] = df_all['All Domains'].apply(
                lambda x: f'<span style="background-color: yellow">{x}</span>' if search_input_all.lower() in x.lower() else x
            )
            st.markdown(f"### 📋 All Domains (With Duplicates) - {total_count}")
            st.write(df_all.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.dataframe(df_all, height=300)

        # Excel export with 2 sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_unique.to_excel(writer, index=False, sheet_name='Unique Domains')
            df_all.to_excel(writer, index=False, sheet_name='All Domains')
        output.seek(0)  # Very important for download to work

        st.download_button(
            label="📥 Download Both Unique and All Domains (Excel with 2 Sheets)",
            data=output.getvalue(),
            file_name="email_domains.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
