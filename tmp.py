from datetime import datetime
import extra_streamlit_components as stx
import streamlit as st

from streamlit_cookies_controller import CookieController

st.set_page_config('Cookie QuickStart', '🍪', layout='wide')

controller = CookieController()
cookie = controller.get('cookie_name')
print(cookie)
# Set a cookie
controller.set('cookie_name', 'testing {}'.format(datetime.now()))

# Get all cookies
cookies = controller.getAll()

# Get a cookie
cookie = controller.get('cookie_name')

# Remove a cookie
controller.remove('cookie_name')
st.write(cookie)