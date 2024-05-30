import streamlit as st
import pandas as pd

st.title('Y Calculation from Weighted Ranks')

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # Display the uploaded file
    st.write("Uploaded Excel file:")
    st.dataframe(df)

    # Ensure required columns are present
    required_columns = ['PSTATABB', 'Plant county name', 'PNAME']
    if not all(col in df.columns for col in required_columns):
        st.error(f"The uploaded file must contain the columns: {', '.join(required_columns)}.")
    else:
        # Dropdown for selecting state code
        state_code = st.selectbox('Select State Code (PSTATABB)', df['PSTATABB'].unique())

        # Filter dataframe based on selected state code
        df_state = df[df['PSTATABB'] == state_code]

        # Dropdown for selecting plant county name
        county_name = st.selectbox('Select Plant County Name', df_state['Plant county name'].unique())

        # Filter dataframe based on selected county name
        df_county = df_state[df_state['Plant county name'] == county_name]

        # Dropdown for selecting plant name
        plant_name = st.selectbox('Select Plant Name (PNAME)', df_county['PNAME'].unique())

        # Filter dataframe based on selected plant name
        df_plant = df_county[df_county['PNAME'] == plant_name]

        # Dropdowns to assign columns to X1 to X5
        st.subheader('Assign columns to X1 to X5:')
        available_columns = df.columns.tolist()

        X1_col = st.selectbox('Select column for X1', available_columns, index=available_columns.index('GEN') if 'GEN' in available_columns else 0)
        X2_col = st.selectbox('Select column for X2', available_columns, index=available_columns.index('PIPE') if 'PIPE' in available_columns else 0)
        X3_col = st.selectbox('Select column for X3', available_columns, index=available_columns.index('MARKET') if 'MARKET' in available_columns else 0)
        X4_col = st.selectbox('Select column for X4', available_columns, index=available_columns.index('INCENTIVES') if 'INCENTIVES' in available_columns else 0)
        X5_col = st.selectbox('Select column for X5', available_columns, index=available_columns.index('WATER') if 'WATER' in available_columns else 0)

        # Extract values for X1 to X5 from the selected row
        X1_value = df_plant[X1_col].values[0]
        X2_value = df_plant[X2_col].values[0]
        X3_value = df_plant[X3_col].values[0]
        X4_value = df_plant[X4_col].values[0]
        X5_value = df_plant[X5_col].values[0]

        # Extract minimum and maximum values for X1 to X5
        X1_min, X1_max = df[X1_col].min(), df[X1_col].max()
        X2_min, X2_max = df[X2_col].min(), df[X2_col].max()
        X3_min, X3_max = df[X3_col].min(), df[X3_col].max()
        X4_min, X4_max = df[X4_col].min(), df[X4_col].max()
        X5_min, X5_max = df[X5_col].min(), df[X5_col].max()

        # Input sliders for weights
        w1 = st.slider("Weight w1", 0, 100, 20) / 100.0
        w2 = st.slider("Weight w2", 0, 100, 20) / 100.0
        w3 = st.slider("Weight w3", 0, 100, 20) / 100.0
        w4 = st.slider("Weight w4", 0, 100, 20) / 100.0
        w5 = st.slider("Weight w5", 0, 100, 20) / 100.0

        # Input sliders for X1 to X5 with dynamic min and max values and default values
        X1 = st.slider(f'Score {X1_col}', float(X1_min), float(X1_max), float(X1_value))
        X2 = st.slider(f'Score {X2_col}', float(X2_min), float(X2_max), float(X2_value))
        X3 = st.slider(f'Score {X3_col}', float(X3_min), float(X3_max), float(X3_value))
        X4 = st.slider(f'Score {X4_col}', float(X4_min), float(X4_max), float(X4_value))
        X5 = st.slider(f'Score {X5_col}', float(X5_min), float(X5_max), float(X5_value))

        # Calculate Y
        Y = (w1 * X1 +
             w2 * X2 +
             w3 * X3 +
             w4 * X4 +
             w5 * X5)

        # Display the result
        st.subheader('Calculated Y Value:')
        st.write(Y)
        
        # Determine the viability threshold dynamically
        max_Y = (w1 * X1_max +
                 w2 * X2_max +
                 w3 * X3_max +
                 w4 * X4_max +
                 w5 * X5_max)

        threshold = max_Y * 0.75

        # Determine if the project is viable
        if Y > threshold:
            st.success("Viable Project")
        else:
            st.warning("Not a viable project")
