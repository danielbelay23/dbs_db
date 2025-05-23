import re
import streamlit as st

def process_skills(skills_list):
    processed_skills = []
    is_hard_skills = any(bullet.startswith("**") for bullet in skills_list)

    for bullet in skills_list:
        if is_hard_skills:
            bullet = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #ffcc00;">\1</strong>', bullet)
        processed_skills.append(bullet)
    
    skills_html = "".join([f"{bullet}</br>" for bullet in processed_skills])
    skills_title = "Hard Skills" if is_hard_skills else "Soft Skills"
    skills_card_html = f"""
    <div class="job-card">
        <div class="job-title">
            <p align="center" style="width:100%; color: #ffcc00; font-size: 1.6rem; font-weight: bold; font-family: 'Montserrat', sans-serif;">{skills_title}</p>
        </div>
        <div class="job-description">
            {skills_html}
        </div>
    </div>
    """
    return skills_card_html

def create_job_card(title, company, location, date_range, bullet_points):
    """
    Creates a styled job card with the given parameters.
    Args:
        title (str): Job title
        company (str): Company name
        location (str): Job location
        date_range (str): Date range of employment
        bullet_points (list): List of bullet point descriptions
    """
    bullets_html = "".join([f"<li>{point}</li>" for point in bullet_points])
    job_card_html = f"""
    <div class="job-card">
        <div class="job-header">
            <div class="job-title">{title}</div>
            <div class="job-company"> | </div>
            <div class="job-company">{company}</div>
        </div>
        <div class="job-date">
            {location} | {date_range}
        </div>
        <div class="job-description">
            <ul>
                {bullets_html}
            </ul>
        </div>
    </div>
    """
    st.markdown(job_card_html, unsafe_allow_html=True)

def create_info_card(title, content):
    """Creates a card-like element with a title and matching color schemes.
    Args:
        title (str): the title of the card
        content (dict): 
            k: title of the bullet point
            v: bullet point description or None
    """
    card_html = f"""<div style='background-color: rgba(26, 26, 46, 0.8); border-radius: 10px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255, 204, 0, 0.2);'>
<h3 style='font-family: Montserrat, sans-serif; color: #ffcc00; font-size: 1.6rem; margin: 0 0 1rem 0;'>{title}</h3>
<div style='font-family: "Fira Code", monospace; color: #e0e0e0;'>
<ul style='list-style: none; padding-left: 0;'>"""
    
    for k, v in content.items():
        if k is None:
            card_html += f"<li style='margin-bottom: 0.8rem;'><span style='color: #ffcc00;'>▪</span> {v} </li>"
        else:
            card_html += f"<li style='margin-bottom: 0.8rem;'><span style='color: #ffcc00;'>▪</span> <strong style='color: #ffcc00;'>{k}</strong>: {v}</li>"
    card_html += "</ul></div></div>"
    st.markdown(card_html, unsafe_allow_html=True)
    
job_card_style = """
<style>
.job-card {
    background-color: #2a2a3a;
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 50px 50px rgba(0, 0, 0, 0.4);
    border-left: 40px solid #ffcc00;
}
.job-header {
    display: flex;
    margin-bottom: 0.1rem;
} 
.job-title {
    color: #ffcc00;
    font-size: 1.35rem;
    font-weight: bold;
    font-family: 'Montserrat', sans-serif;
}
.job-company {
    color: white;
    font-size: 1.35rem;
    font-weight: bold;
    font-family: 'Montserrat', sans-serif;
    margin-left: 1rem;
}
.job-date {
    color: white;
    font-size: 1.35rem;
    font-family: 'Montserrat', sans-serif;
    margin-bottom: .8rem;
}
.job-description {
    color: #e0e0e0;
    line-height: 1.6;
    font-size: 0.9rem;
    font-family: 'Montserrat', sans-serif;
}
.job-description ul {
    margin: 0;
    padding-left: 1.5rem;
    list-style-type: disc;
}
.job-description li {
    margin-bottom: 0.8rem;
    padding-left: 1rem;
    font-family: 'Montserrat', sans-serif;
}
</style>
"""

section_heading_style = """
<style>
h2.section-heading {
    font-family: Montserrat, sans-serif !important;
    text-align: center !important;
    color: #ffcc00 !important;
    margin-top: -2rem !important;
    margin-bottom: 1rem !important;
    margin-left: 0rem !important;
    margin-right: 0rem !important;
    font-size: 1.875rem !important;
    font-weight: bold !important;
}
</style>
"""

def create_section_heading(title):
    """
    Creates a styled section heading with consistent formatting.
    Args:
        title (str): The heading text
    """
    return f"<h2 class='section-heading'>{title}</h2>"

def add_footer():
    st.markdown(
        "<p style='font-family: \"Fira Code\", monospace; color: #9fe2bf; font-size: 0.9em; margin-top: 2em; text-align: center;'>© 2025 Daniel Belay. All rights reserved.</p>",
        unsafe_allow_html=True
    )

