import streamlit as st


def _go_next(page_path: str) -> None:
    if hasattr(st, 'switch_page'):
        st.switch_page(page_path)
    else:
        st.info('Use the sidebar to continue to the next step.')


st.title('Market Insights')
st.caption('Step 4 of 6')
st.write(
    'Explore area-level trends and context to complement the property-level prediction results.'
)

st.divider()
if st.button('Next: Model Explanation', type='primary'):
    _go_next('pages/5_Model_Explanation.py')
