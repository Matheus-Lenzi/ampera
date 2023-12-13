import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import timedelta
from plotly import graph_objects as go


st.set_page_config(layout = "wide")

def read_csv(path):
    dataset = pd.read_csv(path)
    dataset = dataset.drop(columns=dataset.columns.difference(["date_hour", "date", "hour", "timestamp", "position_x", "position_y", "position_z", "latitude", "longitude", "altitude", "speed", "acceleration"]))
    dataset = dataset.dropna(axis="index")
    
    dataset["date_hour"] = pd.to_datetime(dataset["date_hour"])
    dataset["date"] = pd.to_datetime(dataset["date"], format="%d/%m/%Y").dt.date
    dataset["hour"] = pd.to_datetime(dataset["hour"], format="%H:%M:%S:%f").dt.time
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"])

    return dataset

def render_map(layer, dataset):
    
    layers = []

    if layer == "ScatterplotLayer":
        pitch = 0
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data = dataset[["longitude", "latitude"]],
                get_position = ["longitude", "latitude"],
                get_color = [131, 201, 255],
                get_radius = 2.5,
                pickable=True,
            )
        )

    if layer == "HexagonLayer":
        pitch = 50
        layers.append(
            pdk.Layer(
                "HexagonLayer",
                data = dataset[["longitude", "latitude", "altitude"]],
                get_position = ["longitude", "latitude"],
                radius = 2.5,
                auto_highlight = True,
                pickable = True,
                extruded = True,
                elevation_scale = 4,
                elevation_range=[dataset["altitude"].min(), dataset["altitude"].max()],
                coverage = 1,
            )
        )

    st.pydeck_chart(
        pdk.Deck(
            initial_view_state = pdk.ViewState(
                latitude = dataset["latitude"].iloc[0],
                longitude = dataset["longitude"].iloc[0],
                zoom = 15,
                pitch = pitch,
                tilt = 45
            ),
            layers = [layers],
        ),
        use_container_width = True
    )


def main():

    with st.sidebar:

        st.title("Ampera Racing")

        dataset = read_csv("../data/output.csv")
            
        left_top_column, right_top_column = st.columns(2)

        with left_top_column:
            st.metric(label="Total Rows", value=dataset.shape[0])

            start_date = st.date_input("Start date", value=dataset["date"].min(), format="DD/MM/YYYY")
            start_date = pd.to_datetime(start_date).date()

        with right_top_column:
            min_date_hour = dataset["date_hour"].min()
            max_date_hour = dataset["date_hour"].max()

            st.metric(label="Total Duration", value=f"{(max_date_hour - min_date_hour).seconds} s")

            end_date = st.date_input("End date", value=dataset["date"].min(), format="DD/MM/YYYY")
            end_date = pd.to_datetime(end_date).date()

        if start_date <= end_date:
            pass
        else:
            st.error("Error: End date must fall after start date.")

        min_hour_value = dataset["hour"].min() 
            
        max_hour_value=dataset["hour"].max()

        hour = st.slider("Hour:", min_value=min_hour_value, max_value=max_hour_value, value=(min_hour_value, max_hour_value), step = timedelta(seconds = 1), format = "HH:mm:ss")

        layer = st.selectbox("Layer", options=["ScatterplotLayer", "HexagonLayer"])

    dataset = dataset.loc[(dataset["date"] >= start_date) & (dataset["date"] <= end_date) & (dataset["hour"] >= hour[0]) & (dataset["hour"] <= hour[-1])]

    render_map(layer, dataset)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataset['hour'], y=dataset['speed'], mode='lines', name='Speed'))

    fig.update_layout(yaxis=dict(title='Speed', side='left', showgrid=False))

    fig.add_trace(go.Scatter(x=dataset['hour'], y=dataset['acceleration'], mode='lines', name='Acceleration', yaxis='y2'))

    fig.update_layout(yaxis2=dict(title='Acceleration', overlaying='y', side='right', showgrid=False), showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Dataset"):

        st.dataframe(dataset, use_container_width=True)

if __name__ == "__main__":
    main()