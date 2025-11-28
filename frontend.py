# streamlit_frontend.py
import streamlit as st
import requests
import base64
import urllib.parse
import os

st.set_page_config(page_title="Simple Social", layout="wide")

# --- LOCAL TEST FILE (from your session) ---
# Developer note: use this local path as the file URL when backend/post data uses local testing path.
TEST_LOCAL_URL = "/mnt/data/6547e46f-66dd-4e2a-847a-15b99f66cf32.png"

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None


def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login_page():
    st.title("🚀 Welcome to Simple Social")

    # Simple form with two buttons
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if email and password:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                # Login using FastAPI Users JWT endpoint
                login_data = {"username": email, "password": password}
                try:
                    response = requests.post("http://localhost:8000/auth/jwt/login", data=login_data, timeout=10)
                except Exception as e:
                    st.error(f"Login request failed: {e}")
                    return

                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data.get("access_token") or token_data.get("token")

                    # Get user info (FastAPI Users mounted under /auth/users/me)
                    try:
                        user_response = requests.get("http://localhost:8000/auth/users/me", headers=get_headers(), timeout=10)
                    except Exception as e:
                        st.error(f"Failed to get user info: {e}")
                        return

                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                    else:
                        st.error("Failed to get user info")
                else:
                    # Display backend error if present
                    try:
                        err = response.json()
                    except Exception:
                        err = response.text
                    st.error(f"Invalid email or password! ({err})")

        with col2:
            if st.button("Sign Up", type="secondary", use_container_width=True):
                # Register using FastAPI Users
                signup_data = {"email": email, "password": password}
                try:
                    response = requests.post("http://localhost:8000/auth/register", json=signup_data, timeout=10)
                except Exception as e:
                    st.error(f"Registration request failed: {e}")
                    return

                if response.status_code in (200, 201):
                    st.success("Account created! Click Login now.")
                else:
                    try:
                        error_detail = response.json().get("detail", "Registration failed")
                    except Exception:
                        error_detail = response.text
                    st.error(f"Registration failed: {error_detail}")
    else:
        st.info("Enter your email and password above")


def upload_page():
    st.title("📸 Share Something")

    uploaded_file = st.file_uploader("Choose media", type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'])
    caption = st.text_area("Caption:", placeholder="What's on your mind?")

    if uploaded_file and st.button("Share", type="primary"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            try:
                response = requests.post("http://localhost:8000/upload", files=files, data=data, headers=get_headers(), timeout=30)
            except Exception as e:
                st.error(f"Upload request failed: {e}")
                return

            if response.status_code in (200, 201):
                st.success("Posted!")
                st.rerun()
            else:
                # show backend error details
                try:
                    err = response.json()
                except Exception:
                    err = response.text
                st.error(f"Upload failed: {err}")


def encode_text_for_overlay(text):
    """Encode text for ImageKit overlay - base64 then URL encode"""
    if not text:
        return ""
    # Base64 encode the text
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    # URL encode the result
    return urllib.parse.quote(base64_text)


def create_transformed_url(original_url, transformation_params, caption=None):
    """
    Create a transformation URL for ImageKit style service.
    If original_url is a local file path (starts with /mnt/data), return it unchanged
    because Streamlit can display local files directly.
    """
    if not original_url:
        return original_url

    # If this is a local file path (testing fallback), return as-is
    if original_url.startswith("/") or original_url.startswith("file://") or original_url.startswith("C:\\"):
        return original_url

    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        # Add text overlay at bottom with semi-transparent background (ImageKit style)
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")
    if len(parts) < 5:
        return original_url

    imagekit_id = parts[3]
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"


def feed_page():
    st.title("🏠 Feed")

    try:
        response = requests.get("http://localhost:8000/feed", headers=get_headers(), timeout=10)
    except Exception as e:
        st.error(f"Failed to load feed: {e}")
        return

    if response.status_code == 200:
        # Backend returns a list of posts (not wrapped in {"posts": [...]})
        try:
            posts = response.json()
        except Exception:
            st.error("Invalid feed response")
            return

        if not posts:
            st.info("No posts yet! Be the first to share something.")
            return

        for post in posts:
            st.markdown("---")

            # Header with user, date, and delete button (if owner)
            col1, col2 = st.columns([4, 1])
            with col1:
                # If created_at missing, fall back gracefully
                created = post.get('created_at') or ""
                st.markdown(f"**{post.get('email','Unknown')}** • {created[:10]}")
            with col2:
                if post.get('is_owner', False):
                    if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
                        # Delete the post
                        try:
                            del_resp = requests.delete(f"http://localhost:8000/posts/{post['id']}", headers=get_headers(), timeout=10)
                        except Exception as e:
                            st.error(f"Delete request failed: {e}")
                            continue

                        if del_resp.status_code == 200:
                            st.success("Post deleted!")
                            st.rerun()
                        else:
                            try:
                                err = del_resp.json()
                            except Exception:
                                err = del_resp.text
                            st.error(f"Failed to delete post: {err}")

            # Uniform media display with caption overlay
            caption = post.get('caption', '')

            # Use the post URL if present; otherwise fallback to test local file (for local testing)
            post_url = post.get('url') or TEST_LOCAL_URL

            if post.get('file_type') == 'image':
                uniform_url = create_transformed_url(post_url, "", caption)
                # If it's a local path and exists, display directly; else display remote URL
                if uniform_url.startswith("/") and os.path.exists(uniform_url):
                    st.image(uniform_url, width=300, caption=caption)
                else:
                    st.image(uniform_url, width=300, caption=caption)
            else:
                # For videos: specify a transformation or use URL directly
                uniform_video_url = create_transformed_url(post_url, "w-400,h-200,cm-pad_resize,bg-blurred")
                # Streamlit supports both remote and local video paths
                st.video(uniform_video_url, format="video/mp4", start_time=0)
                if caption:
                    st.caption(caption)

            st.markdown("")  # Space between posts
    else:
        try:
            err = response.json()
        except Exception:
            err = response.text
        st.error(f"Failed to load feed: {err}")


# Main app logic
if st.session_state.user is None:
    login_page()
else:
    # Sidebar navigation
    st.sidebar.title(f"👋 Hi {st.session_state.user.get('email','user')}!")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate:", ["🏠 Feed", "📸 Upload"])

    if page == "🏠 Feed":
        feed_page()
    else:
        upload_page()