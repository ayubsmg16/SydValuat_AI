import streamlit as st


def _go_next(page_path: str) -> None:
    if hasattr(st, 'switch_page'):
        st.switch_page(page_path)
    else:
        st.info('Use the sidebar to continue to the next step.')


st.title('Model Explanation')
st.caption('Step 5 of 6')
st.write(
    'Understand how the valuation model works, what features influence predictions, and '
    'how to interpret outputs responsibly.'
)

st.divider()
if st.button('Next: About Project', type='primary'):
    _go_next('pages/6_About_Project.py')
