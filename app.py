import streamlit as st
import pandas as pd
from io import BytesIO

# Page config
st.set_page_config(page_title=" Extract Domain from Email Address", layout="wide")

# Custom CSS for scrollbar and highlight
st.markdown("""
    <style>
    .stDataFrame div::-webkit-scrollbar {
        width: 14px;
    }

    .stDataFrame div::-webkit-scrollbar-track {
        background: white;
    }

    .stDataFrame div::-webkit-scrollbar-thumb {
        background-color: black;
        border-radius: 8px;
        border: 2px solid white;
        min-height: 40px;
    }

    .stDataFrame div::-webkit-scrollbar-thumb:hover {
        background-color: black;
    }

    /* Highlighted instruction text */
    .highlight-instruction {
        background-color: #fdf7d8;
        padding: 10px;
        border: 2px dashed #ffcc00;
        font-size: 16px;
        font-weight: bold;
    }

    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("📧 Extract Domain using Email Address")
st.markdown("Paste up to **1 million emails** (one per line) and click **Extract Domains** to get only the domains.")

# Highlighted instructions
st.markdown("""
    <div class="highlight-instruction">
    📌 **Instructions:**<br>
    Paste the list of email addresses below. Ensure each email is on a new line.<br>
    <br>
    Example:<br>
    <code>caliptorealestate@gmail.com</code><br>
    <code>phillip@caliptoinc.com</code><br>
    <code>karia723@aol.com</code><br>
    <code>clarkbianchi1@gmail.com</code><br>
    <code>nick@bhrec.net</code><br>
    <code>vdavis4466@live.com</code><br>
    <code>larry@larrylawrencerealtor.com</code><br>
    <code>polar1_2000@yahoo.com</code><br>
    <br>
    The first line can be the header or the actual email address. If a header is present, it will be skipped automatically.
    </div>
""", unsafe_allow_html=True)

# Email input
emails_input = st.text_area("Paste your email list here:", height=300, help="Each email on a new line.")

if st.button("🚀 Extract Domains"):
    if not emails_input.strip():
        st.warning("Please paste some emails to extract.")
    else:
        emails = emails_input.strip().splitlines()
        emails = emails[:1_000_000]  # Limit to 1 million

        # Skip header if present
        first_line = emails[0].strip().lower()
        if first_line in ["email", "email address", "emailaddress"]:
            emails = emails[1:]

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
        st.dataframe(df_unique, height=300)

        # Show All Domains (With Duplicates)
        st.markdown(f"### 📋 All Domains (With Duplicates) - {total_count}")
        df_all = pd.DataFrame(domains, columns=["All Domains"])
        st.dataframe(df_all, height=300)

        # Excel export with 2 sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_unique.to_excel(writer, index=False, sheet_name='Unique Domains')
            df_all.to_excel(writer, index=False, sheet_name='All Domains')
        output.seek(0)

        st.download_button(
            label="📥 Download Both Unique and All Domains (Excel with 2 Sheets)",
            data=output.getvalue(),
            file_name="email_domains.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
