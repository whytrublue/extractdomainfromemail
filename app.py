import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Email Domain Extractor", layout="wide")

st.title("📧 Email Domain Extractor")
st.markdown("Paste up to **1 million emails** (one per line) and click **Extract Domains** to get only the domains.")

emails_input = st.text_area("Paste your email list here:", height=300, help="Each email on a new line.")

# Add larger buttons for extraction and search
extract_button = st.button("🚀 Extract Domains", help="Click to extract the domains from your email list.")
search_unique_button = st.button("🔍 Search Unique Domains", help="Search within unique domains.")
search_all_button = st.button("🔍 Search All Domains", help="Search within all domains.")

# Input field for search query
search_query = st.text_input("Enter search query:", help="Enter a domain or keyword to search for.")

if extract_button:
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

        # Show Unique Domains
        st.markdown(f"### ✅ Unique Domains - {unique_count}")
        df_unique = pd.DataFrame(unique_domains, columns=["Unique Domains"])
        if search_query:
            df_unique['Match'] = df_unique['Unique Domains'].apply(lambda x: search_query.lower() in x.lower())
            df_unique = df_unique[df_unique['Match'] == True]
            st.dataframe(df_unique.style.applymap(lambda x: 'background-color: yellow' if x else '', subset=['Unique Domains']), height=300)
        else:
            st.dataframe(df_unique, height=300)

        # Show All Domains (With Duplicates)
        st.markdown(f"### 📋 All Domains (With Duplicates) - {total_count}")
        df_all = pd.DataFrame(domains, columns=["All Domains"])
        if search_query:
            df_all['Match'] = df_all['All Domains'].apply(lambda x: search_query.lower() in x.lower())
            df_all = df_all[df_all['Match'] == True]
            st.dataframe(df_all.style.applymap(lambda x: 'background-color: yellow' if x else '', subset=['All Domains']), height=300)
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
