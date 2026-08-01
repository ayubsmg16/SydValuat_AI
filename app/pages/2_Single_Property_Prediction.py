import streamlit as st


def _go_next(page_path: str) -> None:
    if hasattr(st, 'switch_page'):
        st.switch_page(page_path)
    else:
        st.info('Use the sidebar to continue to the next step.')


st.title('Single Property Prediction')
st.caption('Step 2 of 6')
st.write(
    'Estimate the value of one property at a time using the trained SydValuat_AI pipeline. '
    'Use this page for detailed, property-level checks.'
)

st.divider()
if st.button('Next: Batch Prediction', type='primary'):
    _go_next('pages/3_Batch_Prediction.py')
