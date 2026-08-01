import streamlit as st

st.set_page_config(page_title='SydValuat_AI', layout='centered')

st.title('SydValuat_AI')
st.subheader('Sydney Property Valuation Journey')
st.write(
    'Follow this guided flow: Home → Single Property Prediction → Batch Prediction → '
    'Market Insights → Model Explanation → About Project.'
)
st.caption('Start with Home from the sidebar to begin.')

if hasattr(st, 'navigation') and hasattr(st, 'Page'):
    pages = [
        st.Page('pages/1_Home.py', title='Home'),
        st.Page('pages/2_Single_Property_Prediction.py', title='Single Property Prediction'),
        st.Page('pages/3_Batch_Prediction.py', title='Batch Prediction'),
        st.Page('pages/4_Market_Insights.py', title='Market Insights'),
        st.Page('pages/5_Model_Explanation.py', title='Model Explanation'),
        st.Page('pages/6_About_Project.py', title='About Project'),
    ]
    st.navigation(pages).run()
