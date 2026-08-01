import streamlit as st


def _go_next(page_path: str) -> None:
    if hasattr(st, 'switch_page'):
        st.switch_page(page_path)
    else:
        st.info('Use the sidebar to continue to the next step.')


st.title('Home')
st.caption('Step 1 of 6')
st.write(
    'Welcome to SydValuat_AI. This app helps you move from individual property valuation '
    'to broader market understanding in a simple step-by-step flow.'
)

st.subheader('Journey')
st.markdown(
    '1. Home\n'
    '2. Single Property Prediction\n'
    '3. Batch Prediction\n'
    '4. Market Insights\n'
    '5. Model Explanation\n'
    '6. About Project'
)

st.divider()
if st.button('Next: Single Property Prediction', type='primary'):
    _go_next('pages/2_Single_Property_Prediction.py')
