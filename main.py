import streamlit as st

st.title('Project Viability Calculation from Weighted Ranks')

# Input boxes for weights
st.subheader('Enter the weights (percentiles):')

weights = {}
total_weight = 0
for i in range(1, 6):
    weights[f'w{i}'] = st.number_input(f'Weight w{i} (%)', min_value=0, max_value=100, value=20)
    total_weight += weights[f'w{i}']

# Ensure the weights add up to 100%
if total_weight != 100:
    st.error("The weights must add up to 100 percent.")
else:
    # Convert weights to fractions
    for key in weights:
        weights[key] /= 100.0

    # Sliders for scores
    st.subheader('Adjust the scores:')
    X1 = st.slider('Score X1', 1, 5, 3)
    X2 = st.slider('Score X2', 1, 5, 3)
    X3 = st.slider('Score X3', 1, 5, 3)
    X4 = st.slider('Score X4', 0, 5, 3)  # Adjusted to a maximum score of 5
    X5 = st.slider('Score X5', 0, 1, 1)

    # Calculate Y
    Y = (weights['w1'] * X1 +
         weights['w2'] * X2 +
         weights['w3'] * X3 +
         weights['w4'] * X4 +
         weights['w5'] * X5)

    # Display the result
    st.subheader('Calculated Y Value:')
    st.write(Y)
    
    # Determine the viability threshold dynamically
    max_Y = (weights['w1'] * 5 +
             weights['w2'] * 5 +
             weights['w3'] * 5 +
             weights['w4'] * 5 +  # Adjusted to a maximum score of 5
             weights['w5'] * 1)

    threshold = max_Y * 0.75

    # Determine if the project is viable
    if Y > threshold:
        st.success("Viable Project")
    else:
        st.warning("Not a viable project")
