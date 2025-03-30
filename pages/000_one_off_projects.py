
import streamlit as st
import plotly.graph_objects as go

phases = [
    {"name": "Phase 1", "description": "Kickoff", "color": "#4C78A8"},
    {"name": "Phase 2", "description": "Planning", "color": "#F58518"},
    {"name": "Phase 3", "description": "Execution", "color": "#E45756"},
    {"name": "Phase 4", "description": "Review", "color": "#72B7B2"},
    {"name": "Phase 5", "description": "Testing", "color": "#54A24B"},
    {"name": "Phase 6", "description": "Lorem ipsum...", "color": "#EECA3B"},
]

# data = {
#     "title": "Project Timeline",
#     "events": [
#         {"start": "2012-08-30", "end": "2016-05-10", "location": "Nashville, TN", "content": "Vanderbilt University"},
#         #{"start": "2013-08-01", "end": "2014-05-31", "location": "Nashville, TN", "content": "Vanderbilt University Molecular Physiology & Biophysics Laboratory"},
#         #{"start": "2014-06-01", "end": "2014-08-31", "location": "New York, NY", "content": "Columbia University Internship in Continuing Education"},
#         #{"start": "2014-12-01", "end": "2015-12-31", "location": "Nashville, TN", "content": "Revive Health Care Solutions - Issues & Crisis Analyst"},
#         {"start": "2016-05-01", "end": "2017-02-28", "location": "Washington, D.C.", "content": "The Advisory Board Company - Business Analyst"},
#         {"start": "2017-02-01", "end": "2019-01-31", "location": "San Francisco, CA", "content": "Triage Consulting Group - Senior Consultant"},
#         {"start": "2019-01-01", "end": "2020-08-31", "location": "Redwood City, CA", "content": "Bluevine Capital - Senior Business Data Operations Analyst"},
#         {"start": "2021-01-01", "end": "Present", "location": "Austin, TX", "content": "Guideline 401(k) - Senior Staff Data Analyst"}
#     ]
# }

fig = go.Figure()

y0 = 0.3   
y1 = 0.7   
y_mid = 0.5

for i, phase in enumerate(phases):
    x0 = i / len(phases)
    x1 = (i + 1) / len(phases)
    offset = (x1 - x0) * 0.2

    path = (
        f"M {x0} {y0} "            
        f"L {x1 - offset} {y0} "   
        f"L {x1} {y_mid} "         
        f"L {x1 - offset} {y1} "   
        f"L {x0} {y1} "            
        "Z"                        
    )

    fig.add_shape(
        type="path",
        path=path,
        fillcolor=phase["color"],
        line_color=phase["color"]
    )

    fig.add_annotation(
        x=(x0 + x1) / 2,
        y=y_mid,
        text=phase["name"],
        showarrow=False,
        font=dict(size=20, color="white"),
        xanchor="right",
        yanchor="middle"
    )

    if "description" in phase and phase["description"]:
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=y1 + 0.02, 
            text=phase["description"],
            showarrow=False,
            font=dict(size=15, color="white"),
            xanchor="center",
            yanchor="bottom"
        )

fig.update_xaxes(visible=False, range=[0, 1])
fig.update_yaxes(visible=False, range=[0, 1])

fig.update_layout(
    width=900,
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)
st.stop()
