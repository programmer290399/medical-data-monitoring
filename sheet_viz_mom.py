import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data_path = "https://docs.google.com/spreadsheets/d/1QUitUwxUuxBXdyyrICIsZa2AQbvVxkH8jobi1qPs8u0/edit#gid=295594796"
url = data_path.replace("/edit#gid=", "/export?format=csv&gid=")


def make_graph(grp_name, grp):
    grp["hour"] = grp["Timestamp"].apply(lambda x: x.hour)

    if grp_name != "Blood Pressure (SYS,DIA)":
        fig = go.Figure()
        grp["Recorded Value"] = pd.to_numeric(grp["Recorded Value"])
        grp["sma"] = grp["Recorded Value"].rolling(9).mean().rolling(5).mean()

        fig.add_trace(
            go.Scatter(
                name="Raw Data",
                x=grp["Timestamp"],
                y=grp["Recorded Value"],
                mode="markers+lines",
                hovertemplate="%{y}",
                marker=dict(
                    color=grp["hour"],
                    colorscale="algae",
                    size=10,
                    colorbar=dict(thickness=10, title="Hour", titleside="top"),
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                name=f"Trend",
                x=grp["Timestamp"],
                y=grp["sma"],
                mode="lines",
                hovertemplate="%{y}",
            )
        )

        fig.update_layout(hovermode="x unified")
        layout = dict(
            width=640,
            height=360,
            title=grp_name,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        fig.update_layout(layout)
        return [fig]
    else:
        figsys = go.Figure()
        figdia = go.Figure()
        grp[["SYS", "DIA"]] = grp["Recorded Value"].str.split(",", 1, expand=True)
        grp["SYS"] = pd.to_numeric(grp["SYS"])
        grp["DIA"] = pd.to_numeric(grp["DIA"])
        grp["sma_sys"] = grp["SYS"].rolling(9).mean().rolling(5).mean()
        grp["sma_dia"] = grp["DIA"].rolling(9).mean().rolling(5).mean()
        figsys.add_trace(
            go.Scatter(
                name="Raw Data",
                x=grp["Timestamp"],
                y=grp["SYS"],
                mode="markers+lines",
                hovertemplate="%{y}",
                marker=dict(
                    color=grp["hour"],
                    colorscale="algae",
                    size=10,
                    colorbar=dict(thickness=10, title="Hour", titleside="top"),
                ),
            )
        )
        figsys.add_trace(
            go.Scatter(
                name=f"Trend",
                x=grp["Timestamp"],
                y=grp["sma_sys"],
                mode="lines",
                hovertemplate="%{y}",
            )
        )
        figdia.add_trace(
            go.Scatter(
                name="Raw Data",
                x=grp["Timestamp"],
                y=grp["DIA"],
                mode="markers+lines",
                hovertemplate="%{y}",
                marker=dict(
                    color=grp["hour"],
                    colorscale="algae",
                    size=10,
                    colorbar=dict(thickness=10, title="Hour", titleside="top"),
                ),
            )
        )
        figdia.add_trace(
            go.Scatter(
                name=f"Trend",
                x=grp["Timestamp"],
                y=grp["sma_dia"],
                mode="lines",
                hovertemplate="%{y}",
            )
        )
        layout_sys = dict(
            width=1500,
            height=600,
            title="Blood Pressure - SYS",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        layout_dia = dict(
            width=1500,
            height=600,
            title="Blood Pressure - DIA",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        figsys.update_layout(hovermode="x unified")
        figsys.update_layout(layout_sys)
        figdia.update_layout(hovermode="x unified")
        figdia.update_layout(layout_dia)
        return [figsys, figdia]


def get_graphs():
    graphs = []
    data = pd.read_csv(url)
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])
    grouped = data.groupby("Test Type")
    for name, group in grouped:
        if len(group) > 5:
            graphs.extend(make_graph(name, group))
    return graphs


st.set_page_config(
    page_title="Medical Monitoring System",
    layout="wide",
)
# medical-viz@mom-streamlit-app.iam.gserviceaccount.com

if st.button("Fetch Data"):
    with st.spinner("Fetching Data..."):
        graphs = get_graphs()
    for graph in graphs:
        st.plotly_chart(graph, use_container_width=True)
