"""Default Streamlit Cloud entrypoint.

Streamlit Community Cloud looks for `streamlit_app.py` by default.
This module simply runs the existing UI from `web_app.py`.
"""

from web_app import *  # noqa: F401,F403
