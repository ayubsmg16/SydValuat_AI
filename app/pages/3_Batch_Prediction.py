import streamlit as st


def _go_next(page_path: str) -> None:
    if hasattr(st, 'switch_page'):
        st.switch_page(page_path)
    else:
        st.info('Use the sidebar to continue to the next step.')


st.title('Batch Prediction')
st.caption('Step 3 of 6')
st.write(
    'Run predictions for multiple properties in one pass for faster portfolio-level analysis.'
)

st.divider()
if st.button('Next: Market Insights', type='primary'):
    _go_next('pages/4_Market_Insights.py')
