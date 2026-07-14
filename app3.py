import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# -----------------------------
# PASSWORD CONFIG
# -----------------------------

##PASSWORD = "MyQADashboard123"

# -----------------------------
# SESSION STATE
# -----------------------------

#if "authenticated" not in st.session_state:
 #   st.session_state.authenticated = False


# -----------------------------
# LOGIN SCREEN
# -----------------------------

##if not st.session_state.authenticated:

  #  st.title("QA KPI Dashboard Login")

   # password = st.text_input(
      #  "Enter Password",
   #     type="password"
    #)

  #  if password == PASSWORD:
#        st.session_state.authenticated = True
 #       st.rerun()

  #  elif password:
   #     st.error("Invalid Password")

    #st.stop()


# -----------------------------
# DASHBOARD STARTS HERE
# -----------------------------

st.set_page_config(
    page_title="QA KPI Dashboard",
    layout="wide"
)

st.set_page_config(
    page_title="QA KPI Dashboard",
    layout="wide"
)

from PIL import Image

# Load logos
qentelli_logo = Image.open("Qentelli logo.png")
rp_logo = Image.open("rp logo.png")

# Create top layout
col1, col2, col3 = st.columns([2,4,2])

with col1:
    st.image(qentelli_logo, width=150)

with col2:
    st.markdown(
        "<h1 style='text-align:center;'>QA KPI Dashboard</h1>",
        unsafe_allow_html=True
    )

with col3:
    st.image(rp_logo, width=150)

df = pd.read_csv("qa_kpi_data_v2.csv")

week = st.selectbox("Select Week", df["Week"])

data = df[df["Week"] == week].iloc[0]

# KPI calculations

attrition = (data["Employees Left"] / data["Total Employees"]) * 100

ddr = (data["Defects Detected"] /
       (data["Defects Detected"] + data["Defects Missed"])) * 100

utilization = (data["Billable Hours"] / data["Total Hours"]) * 100

productivity = (data["Completed Hours"] /
                (data["Completed Hours"] + data["Remaining Hours"])) * 100

pass_rate = (data["Test Cases with No Defects"] / data["Test Cases Executed"]) * 100

defect_leakage = (data["Defects UAT"] /
                  (data["Defects QA"] + data["Defects UAT"])) * 100

execution_rate = (data["Test Cases Executed"] / data["Total Test Cases"]) * 100

test_effectiveness = (
    data["Test Cases with No Defects"] /
    data["Test Cases Executed"]
) * 100

coverage = (data["Total Test Cases"] /
            data["Test Cases Designed"]) * 100


# KPI cards
st.subheader("Weekly KPI Snapshot")

col1, col2, col3 = st.columns(3)
col1.metric("Attrition Rate", f"{attrition:.2f}%")
col2.metric("Defect Detection Rate", f"{ddr:.2f}%")
col3.metric("Employee Utilization", f"{utilization:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Productivity Rate", f"{productivity:.2f}%")
col5.metric("QA Test Pass Rate", f"{pass_rate:.2f}%")
col6.metric("Defect Leakage", f"{defect_leakage:.2f}%")

col7, col8, col9 = st.columns(3)
col7.metric("Test Execution Rate", f"{execution_rate:.2f}%")
col8.metric("Test Case Effectiveness", f"{test_effectiveness:.2f}%")
col9.metric("Test Coverage", f"{coverage:.2f}%")


st.subheader("KPI Visualizations")

# -----------------------------
# Doughnut chart function
# -----------------------------

def donut_chart(
        title,
        achieved,
        remaining,
        achieved_label,
        remaining_label,
        achieved_color="#2E8B57",
        remaining_color="#DC143C"
):

    fig = go.Figure(data=[go.Pie(

        labels=[
            f"{achieved_label}: {achieved}",
            f"{remaining_label}: {remaining}"
        ],

        values=[achieved, remaining],

        hole=.70,

        marker=dict(
            colors=[
                achieved_color,
                remaining_color
            ]
        ),

        textinfo='percent',

        hovertemplate='%{label}<br>%{percent}',

        sort=False
    )])

    fig.update_layout(

        title=dict(
            text=title,
            x=0.5,   # center align title
            xanchor='center'
        ),

        height=320,
        width=320,

        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor="center"
        ),

        margin=dict(
            l=10,
            r=10,
            t=50,
            b=60
        )
    )

    return fig

# -----------------------------
# Row1
# -----------------------------

c1,c2,c3=st.columns(3)

c1.plotly_chart(

    donut_chart(
        "Attrition Rate",

        data["Total Employees"]
        - data["Employees Left"],

        data["Employees Left"],

        "Employees Retained",

        "Employees Left",

        "#2E8B57",   # retained green
        "#DC143C"    # left red
    ),

    use_container_width=True
)

c2.plotly_chart(

    donut_chart(
        "Defect Detection Rate",

        data["Defects Detected"],

        data["Defects Missed"],

        "Detected",

        "Missed"
    ),

    use_container_width=True
)

c3.plotly_chart(

    donut_chart(
        "Employee Utilization",

        data["Billable Hours"],

        data["Total Hours"]
        -data["Billable Hours"],

        "Billable Hours",

        "Available Hours"
    ),

    use_container_width=True
)


# -----------------------------
# Row2
# -----------------------------

c4,c5,c6=st.columns(3)

c4.plotly_chart(

    donut_chart(
        "Productivity Rate",

        data["Completed Hours"],

        data["Remaining Hours"],

        "Completed",

        "Remaining"
    ),

    use_container_width=True
)


c5.plotly_chart(

    donut_chart(
        "QA Test Pass Rate",

        data["Test Cases with No Defects"],

        data["Test Cases Executed"]
        - data["Test Cases with No Defects"],

        "Passed",

        "Failed",

        "#2E8B57",   # green = passed
        "#DC143C"    # red = failed
    ),

    use_container_width=True
)


c6.plotly_chart(

    donut_chart(
        "Defect Leakage",

        data["Defects QA"],

        data["Defects UAT"],

        "QA Bugs",

        "UAT Bugs",

        "#2E8B57",   # QA caught bugs = good
        "#DC143C"    # UAT bugs = escaped defects
    ),

    use_container_width=True
)


# -----------------------------
# Row3
# -----------------------------

c7,c8,c9=st.columns(3)

c7.plotly_chart(

    donut_chart(
        "Test Case Effectiveness",

        data["Test Cases with No Defects"],

        data["Test Cases Resulting in Defect Detection"],

        "No Defects",

        "Defects Found",

        "#2E8B57",   # Green = No defects
        "#DC143C"    # Red = Defects found
    ),

    use_container_width=True
)

c8.plotly_chart(

    donut_chart(
        "Test Coverage",

        data["Total Test Cases"],

        data["Test Cases Designed"]
        -data["Total Test Cases"],

        "Covered",

        "Remaining"
    ),

    use_container_width=True
)

c9.plotly_chart(

    donut_chart(

        "Test Execution Rate",

        data["Test Cases Executed"],

        data["Test Cases Not Executed"],

        f"Executed: {data['Test Cases Executed']}",

        f"Not Executed: {data['Test Cases Not Executed']}",

        "#2E8B57",      # Green
        "#DC143C"       # Red
    ),

    use_container_width=True
)

st.subheader("Sprint Velocity")

velocity_fig = go.Figure()

# Completed story points
velocity_fig.add_trace(go.Bar(
    x=df["Week"],
    y=df["Completed Story Points"],
    name="Completed",
    marker_color="#2E8B57",

    text=df["Completed Story Points"],
    textposition="outside"
))

# Committed story points
velocity_fig.add_trace(go.Bar(
    x=df["Week"],
    y=df["Committed Story Points"],
    name="Committed",
    marker_color="#1E90FF",

    text=df["Committed Story Points"],
    textposition="outside"
))

velocity_fig.update_layout(

    barmode='group',

    title=dict(
        text="Sprint Velocity",
        x=0.5,
        xanchor="center"
    ),

    height=420,

    yaxis_title="Story Points",

    legend=dict(
        orientation="h",
        y=-0.2,
        x=0.5,
        xanchor="center"
    )
)

st.plotly_chart(
    velocity_fig,
    use_container_width=True
)

st.subheader("Sprint Burndown")

burndown_fig = go.Figure()

# Ideal burndown
burndown_fig.add_trace(go.Scatter(

    x=df["Week"],
    y=df["Planned Remaining"],

    mode='lines+markers+text',

    name='Ideal Burndown',

    line=dict(color="#1E90FF"),

    text=df["Planned Remaining"],
    textposition="top center"
))

# Actual burndown
burndown_fig.add_trace(go.Scatter(

    x=df["Week"],
    y=df["Actual Remaining"],

    mode='lines+markers+text',

    name='Actual Burndown',

    line=dict(color="#2E8B57"),

    text=df["Actual Remaining"],
    textposition="bottom center"
))

burndown_fig.update_layout(

    title=dict(
        text="Sprint Burndown",
        x=0.5,
        xanchor="center"
    ),

    height=420,

    yaxis_title="Remaining Work",

    legend=dict(
        orientation="h",
        y=-0.2,
        x=0.5,
        xanchor="center"
    )
)

st.plotly_chart(
    burndown_fig,
    use_container_width=True
)
