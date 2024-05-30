import streamlit as st
import pandas as pd
import numpy as np

st.title('Monte Carlo Simulation for Selected State')

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # Display the uploaded file
    st.write("Uploaded Excel file:")
    st.dataframe(df)

    # Ensure required columns are present
    required_columns = ['PSTATABB', 'Plant county name', 'PNAME', 'GEN', 'PIPE', 'MARKET', 'INCENTIVES', 'WATER']
    if not all(col in df.columns for col in required_columns):
        st.error(f"The uploaded file must contain the columns: {', '.join(required_columns)}.")
    else:
        # Dropdown for selecting state code
        state_code_options = ["All"] + df['PSTATABB'].unique().tolist()
        state_code = st.selectbox('Select State Code (PSTATABB)', state_code_options)

        if state_code != "All":
            df_state = df[df['PSTATABB'] == state_code]
        else:
            df_state = df.copy()

        # Dropdown for selecting county
        county_options = ["All"] + df_state['Plant county name'].unique().tolist()
        county = st.selectbox('Select County', county_options)

        if county != "All":
            df_state = df_state[df_state['Plant county name'] == county]

        # Dropdown for selecting plant name
        plant_options = ["All"] + df_state['PNAME'].unique().tolist()
        plant = st.selectbox('Select Plant Name', plant_options)

        if plant != "All":
            df_state = df_state[df_state['PNAME'] == plant]

        # Select columns for the Monte Carlo simulation
        st.subheader('Select columns for Monte Carlo simulation:')
        X1_col = st.selectbox('Select column for X1', df.columns, index=df.columns.get_loc('GEN'))
        X2_col = st.selectbox('Select column for X2', df.columns, index=df.columns.get_loc('PIPE'))
        X3_col = st.selectbox('Select column for X3', df.columns, index=df.columns.get_loc('MARKET'))
        X4_col = st.selectbox('Select column for X4', df.columns, index=df.columns.get_loc('INCENTIVES'))
        X5_col = st.selectbox('Select column for X5', df.columns, index=df.columns.get_loc('WATER'))

        # Input sliders for weights
        w1 = st.slider("Weight w1", 0, 100, 20) / 100.0
        w2 = st.slider("Weight w2", 0, 100, 20) / 100.0
        w3 = st.slider("Weight w3", 0, 100, 20) / 100.0
        w4 = st.slider("Weight w4", 0, 100, 20) / 100.0
        w5 = st.slider("Weight w5", 0, 100, 20) / 100.0

        # Number of simulations
        num_simulations = st.number_input('Number of simulations', min_value=100, max_value=10000, value=1000)

        # Perform Monte Carlo simulation
        if st.button('Run Simulation'):
            X1_samples = np.random.choice(df_state[X1_col], num_simulations)
            X2_samples = np.random.choice(df_state[X2_col], num_simulations)
            X3_samples = np.random.choice(df_state[X3_col], num_simulations)
            X4_samples = np.random.choice(df_state[X4_col], num_simulations)
            X5_samples = np.random.choice(df_state[X5_col], num_simulations)

            # Calculate Y for each simulation
            Y_simulations = (w1 * X1_samples +
                             w2 * X2_samples +
                             w3 * X3_samples +
                             w4 * X4_samples +
                             w5 * X5_samples)

            # Average Y value from simulations
            Y_mean = np.mean(Y_simulations)

            # Display results
            st.subheader('Simulation Results')
            st.write(f'Average Y value from {num_simulations} simulations: {Y_mean}')

            # Determine the viability threshold dynamically
            max_Y = (w1 * df_state[X1_col].max() +
                     w2 * df_state[X2_col].max() +
                     w3 * df_state[X3_col].max() +
                     w4 * df_state[X4_col].max() +
                     w5 * df_state[X5_col].max())

            threshold = max_Y * 0.75

            # Determine if the project is viable
            if Y_mean > threshold:
                st.success("Viable Project")
            else:
                st.warning("Not a viable project")

        # Box for user to input the size of the list
        list_size = st.number_input('Enter the size of the list', min_value=1, max_value=100, value=10, step=1)

        # Calculate Y for all plants in the filtered dataframe
        df_state['Y'] = (w1 * df_state[X1_col] +
                         w2 * df_state[X2_col] +
                         w3 * df_state[X3_col] +
                         w4 * df_state[X4_col] +
                         w5 * df_state[X5_col])

        # Recompute threshold for overall viability
        overall_max_Y = (w1 * df[X1_col].max() +
                         w2 * df[X2_col].max() +
                         w3 * df[X3_col].max() +
                         w4 * df[X4_col].max() +
                         w5 * df[X5_col].max())

        threshold = overall_max_Y * 0.75

        df_state['Viability'] = df_state['Y'].apply(lambda y: 'Viable' if y > threshold else 'Not Viable')

        # Sort dataframe by Y in descending order and get the top entries
        top_df = df_state.nlargest(list_size, 'Y')

        # Display the top entries
        st.subheader('Top Y Scores:')
        st.dataframe(top_df[['PSTATABB', 'Plant county name', 'PNAME', 'Y', 'Viability']])
