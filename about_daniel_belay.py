import os 
import streamlit as st
import re
from src import asset_dir
from PIL import Image
from src.st_server_utils import create_navigation

from src.text_utils import process_skills, create_job_card, job_card_style, create_section_heading, section_heading_style, add_footer
#from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext
#import openai
#from langchain.chat_models import ChatOpenAI

##################  PATH SETTINGS  ##################
profile_pic = os.path.join(asset_dir, "profile-pic.png")
resume_file = os.path.join(asset_dir, "daniel_belay_resume.pdf")
css_file = os.path.join(asset_dir, "styling.css")

##################  GENERAL SETTINGS  ##################
interests = [
    "Enjoy going down rabbit holes—getting lost in the fun and coming out with something interesting",
    "Training for my EMT license (for fun, not for work)", 
    "Working with CASA of Travis County about ~15hr/month", 
    "Used to run marathons and half marathons, now I just talk about having done them", 
    "Sometimes watch reality tv (I'm not proud of this)", 
    "Interested in MLOps and LLMs, but definitely not an expert",
]
profile_info = {
    "PAGE_TITLE": "danielbelay | my horsin' around work",
    "PAGE_ICON": ":wave:",
    "NAME": "Daniel Belay",
    "ROLE": "Senior Staff Data Analyst", 
    "DESCRIPTION": "Assisting enterprises by supporting data-driven decision-making, automating processes, and building scalable data pipelines.",
    "ABOUT_ME": f"▪ {interests[0]}\n▪ {interests[1]}\n▪ {interests[2]}\n▪ {interests[3]}\n▪ {interests[4]}\n▪ {interests[5]}",
    "EMAIL": "danielkbelay2@gmail.com",
    "LOCATED": "Austin, TX",
    "FROM": "Las Vegas, NV", 
    "EDUCATION": "B.S. Economics, Vanderbilt University",
    "GITHUB": "github.com/danielbelay23",
}
projects = [
    "🏆 Built an anomaly detection system that links denied Stripe collections to asset sales, allowing the FinOps team to repurchase assets and wait until collections are enabled",
    "🏆 Created a Sales compensation workflow that records monthly commissions and has the flexibility to include spiffs",
]

st.set_page_config(
    page_title=profile_info["PAGE_TITLE"], 
    page_icon=profile_info["PAGE_ICON"], 
    layout="wide",
    initial_sidebar_state="expanded",
)
create_navigation()
################### STYLING AND PROFILE PICTURE ##################

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)

################## ABOUT ME AND CONTACT INFO ################## 
col1, right_container = st.columns([1, 2])
with col1:
    st.image(profile_pic, width=400)

with right_container:
    st.markdown(
        f"<h1 style='font-family: Montserrat, sans-serif; letter-spacing: 0.05em; font-size: 3.75rem; margin-bottom: 0.5rem;'>{profile_info['NAME']}</h1>",
        unsafe_allow_html=True
    ) 
    col2, col3 = st.columns([2, 2])
    with col2:
        st.markdown(
            f"""
            <div style='font-family: Montserrat, sans-serif;'>
                <h3 style='color: #ffcc00; font-size: 1.8rem; margin: 0 0 0.5rem 0; text-align: center;'>{profile_info['ROLE']}</h3>
                <p style='font-size: 0.9rem; margin: 0 0 0.5rem 0; line-height: 1.3;'>{profile_info['DESCRIPTION']}</p>
                <p style='font-size: 0.9rem; margin: 0 0 0.3rem 0;'>📌 {profile_info['LOCATED']} | 👶🏾 {profile_info['FROM']}</p>
                <p style='font-size: 0.9rem; margin: 0 0 0.3rem 0;'>👨🏾‍🎓 {profile_info['EDUCATION']}</p>
                <p style='font-size: 0.9rem; margin: 0 0 0.3rem 0;'>📬 <a href='mailto:{profile_info['EMAIL']}' style='color: dark blue; text-decoration: none;'>{profile_info['EMAIL']}</a></p>
                <p style='font-size: 0.9rem; margin: 0 0 0.5rem 0;'>👨‍💻 <a href='https://{profile_info['GITHUB']}' target='_blank' style='color: dark blue; text-decoration: none;'>{profile_info['GITHUB']}</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label=" 📄 Download Resume",
            data=PDFbyte,
            file_name="daniel_belay_resume.pdf",
            mime="application/pdf",
            key="download_resume",
            type="secondary",
        )
    
    with col3:
        st.markdown(
            f"""
            <div style='font-family: Montserrat, sans-serif;'>
                <h3 style='color: #ffcc00; font-size: 1.8rem; margin: 0 0 0.5rem 0; text-align: center;'>About me</h3>
                <div style='font-size: 0.9rem; line-height: 1.3;'>
                    {profile_info['ABOUT_ME'].replace('▪', '<p style="margin: 0 0 0.3rem 0;">▪')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

##################  SKILLS  ##################
st.divider()

hard_skills_list = [
    "**👩‍💻 Programming:** Python (scikit-learn, pandas, Airflow, Streamlit, Jenkins), dbt, SQL, JavaScript", 
    "**📊 Data Viz:** Looker (Admin), Tableau, Plotly",
    "**🛠️ Tools:** Salesforce Admin, Pendo, Segment, Git, dbt, Jenkins",
    "**📚 Modeling:** Logistic Regression, Hypothesis Testing, Correlation Analysis, Decision Trees",
    "**🗄️ Databases:** Postgres, MySQL, BigQuery, AWS Redshift, Snowflake"
]
soft_skills_list = [
    "📝 Strong stakeholder communication via project docs, status updates, weekly syncs, and ad-hoc conversations",
    "📣 Effective communication skills for conveying technical concepts to stakeholders and non-technical teams",
    "⏳ Great time management skills, balancing multiple projects and priorities in fast-paced environments",
    "👥 Leadership skills in onboarding new team members"
]

col1, col2 = st.columns([2, 2])
with col1:
    st.markdown(process_skills(hard_skills_list), unsafe_allow_html=True)
with col2:
    st.markdown(process_skills(soft_skills_list), unsafe_allow_html=True)

##################  WORK HISTORY  ##################
st.divider()
st.markdown(job_card_style, unsafe_allow_html=True)
st.markdown(section_heading_style, unsafe_allow_html=True)
st.markdown(create_section_heading("Work History"), unsafe_allow_html=True)

career_dict = {
    "job1": {
        "company": "Guideline 401(k)",
        "title": "Senior Staff Data Analyst",
        "location": "Austin, TX",
        "date": "January 2021 – Present",
        "descriptions": [
            "Developed a self-hosted accounting portal using Streamlit, integrated with Google SSO, featuring monthly subledger summaries, downloadable line items, AR aging reports, and point-in-time accounting snapshot capabilities.",
            "Architected revenue-specific data pipelines and tables (using dbt and Jenkins)–ultimately leading to a Core Metrics dashboard reporting on ARR, AUM, lead count, churn, etc., distributed to the C-Suite and Board of Directors daily.",
            "Led the migration of our MySQL pipeline into team-specific data marts utilizing DBT, Docker, and Jenkins, focusing on reducing Google Cloud (GCP) cost, SOC 2 compliance, and enhancing the data experience for business analysts.",
            "Enabled the rollout of personal and SEP IRA products by creating error detection systems using BigQuery, Sentry, and Honeycomb, checking for: invoice accuracy, failed ACH remediation, and Required Minimum Distributions.",
            "Managed the administration and optimization of Looker and BigQuery platforms."
        ]
    },
    "job2": {
        "company": "Bluevine Capital", 
        "title": "Senior Business Data Operations Analyst",
        "location": "Redwood City, CA",
        "date": "January 2019 – August 2020",
        "descriptions": [
            "Offboarded a third-party lead routing tool and developed an internal lead routing script optimizing lead distribution based on sales channel, in-office status, seniority, MQL status, partnership referrals, and AE/SDR availability.",
            "Organized a cross-functional retention council to analyze LTV, onboarding health, conversion rates, NPS, and churn– culminating in a Retention Health Index and dashboard to highlight pricing optimizations and discount eligibility.",
            "Built and maintained data pipelines in Redshift and Snowflake to support the new banking product, with a primary focus on integrating the product into Salesforce for GTM visibility and operational reporting."
        ]
    },
    "job3": {
        "company": "Triage Consulting Group",
        "title": "Senior Consultant",
        "location": "San Francisco, CA",
        "date": "February 2017 – January 2019",
        "descriptions": [
            "Designed workflows in Microsoft Access, T-SQL, and VBA to detect underpayments and discrepancies between contracted insurance pricing and hospital billing, reducing manual billing review and improving recovery accuracy.",
            "Created and presented quarterly status meetings to hospital finance executives, including revenue forecasts, bulk claim resubmission updates, and opportunities to expedite the identification of medical billing issues."
        ]
    },
    "job4": {
        "company": "Advisory Board Company",
        "title": "Business Analyst",
        "location": "Washington, D.C.",
        "date": "May 2016 – February 2017",
        "descriptions": [
            "Implemented and analyzed “iRound”—a real-time patient satisfaction software used to collect patient satisfaction.",
            "Conducted market research of hospital spending relative to local, regional, and national competitors."
        ]
    },
    "job5": {
        "company": "Revive Health Care Solutions",
        "title": "Issues & Crisis Analyst",
        "location": "Nashville, TN",
        "date": "December 2014 – December 2015",
        "descriptions": [
            "Analyzed and researched hospital performance data via SQL to determine a risk index for joint surgeries.",
            "Strategized solutions and options in hospital-insurer issues & crisis situations with a team of five members.",
        ]
    }
}

for job in career_dict.values():
    create_job_card(
        title=job["title"],
        company=job["company"],
        location=job["location"],
        date_range=job["date"],
        bullet_points=job["descriptions"]
    )

##################  PROJECTS & ACCOMPLISHMENTS  ################## 
st.divider()
st.markdown(create_section_heading("Other Projects"), unsafe_allow_html=True)
for project in projects:
    st.write(project)

add_footer()