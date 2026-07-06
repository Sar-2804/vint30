# ==========================================
# Instagram Clone - Part 1
# app.py
# ==========================================

import streamlit as st
import sqlite3
import hashlib
import os
import uuid
from datetime import datetime
from PIL import Image

# ------------------------------------------
# Page Config
# ------------------------------------------

st.set_page_config(
    page_title="Instagram Clone",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------
# Folders
# ------------------------------------------

UPLOAD_FOLDER = "uploads"
PROFILE_FOLDER = "profiles"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROFILE_FOLDER, exist_ok=True)

# ------------------------------------------
# Database
# ------------------------------------------

conn = sqlite3.connect(
    "instagram.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ------------------------------------------
# Users Table
# ------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT UNIQUE,

fullname TEXT,

email TEXT UNIQUE,

password TEXT,

bio TEXT DEFAULT '',

profile_pic TEXT DEFAULT '',

followers INTEGER DEFAULT 0,

following INTEGER DEFAULT 0,

joined TEXT

)
""")

# ------------------------------------------
# Posts Table
# ------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

image TEXT,

caption TEXT,

likes INTEGER DEFAULT 0,

created TEXT

)
""")

# ------------------------------------------
# Comments Table
# ------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments(

id INTEGER PRIMARY KEY AUTOINCREMENT,

post_id INTEGER,

username TEXT,

comment TEXT,

created TEXT

)
""")

# ------------------------------------------
# Followers Table
# ------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS follows(

id INTEGER PRIMARY KEY AUTOINCREMENT,

follower TEXT,

following TEXT

)
""")

conn.commit()

# ------------------------------------------
# Password Hash
# ------------------------------------------

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# ------------------------------------------
# User Exists
# ------------------------------------------

def user_exists(username):

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    return cursor.fetchone()

# ------------------------------------------
# Create User
# ------------------------------------------

def create_user(
        username,
        fullname,
        email,
        password
):

    cursor.execute(
        """
        INSERT INTO users(
        username,
        fullname,
        email,
        password,
        joined
        )

        VALUES(?,?,?,?,?)
        """,

        (
            username,
            fullname,
            email,
            hash_password(password),
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )
        )
    )

    conn.commit()

# ------------------------------------------
# Login
# ------------------------------------------

def login(username,password):

    cursor.execute(

        """
        SELECT *
        FROM users

        WHERE username=?

        AND password=?
        """,

        (
            username,
            hash_password(password)
        )

    )

    return cursor.fetchone()

# ------------------------------------------
# Upload Image
# ------------------------------------------

def save_image(file):

    ext = file.name.split(".")[-1]

    filename = str(uuid.uuid4()) + "." + ext

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(path,"wb") as f:
        f.write(file.read())

    return path

# ------------------------------------------
# Profile Upload
# ------------------------------------------

def save_profile(file):

    ext = file.name.split(".")[-1]

    filename = str(uuid.uuid4()) + "." + ext

    path = os.path.join(
        PROFILE_FOLDER,
        filename
    )

    with open(path,"wb") as f:
        f.write(file.read())

    return path

# ------------------------------------------
# Session
# ------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

# ------------------------------------------
# Instagram CSS
# ------------------------------------------

st.markdown("""

<style>

body{

background:#fafafa;

}

header{

visibility:hidden;

}

footer{

visibility:hidden;

}

#MainMenu{

visibility:hidden;

}

.main{

padding-top:0rem;

}

.logo{

font-size:38px;

font-weight:bold;

text-align:center;

font-family:cursive;

margin-bottom:20px;

}

.card{

background:white;

padding:20px;

border-radius:15px;

box-shadow:0 2px 12px rgba(0,0,0,.08);

margin-bottom:20px;

}

.profile{

border-radius:50%;

width:60px;

height:60px;

}

.post{

border-radius:12px;

overflow:hidden;

border:1px solid #ddd;

}

.like{

color:red;

font-size:20px;

}

.comment{

background:#f2f2f2;

padding:8px;

border-radius:10px;

margin-top:5px;

}

.follow{

background:#0095f6;

color:white;

padding:8px;

border-radius:8px;

text-align:center;

}

input{

border-radius:10px !important;

}

textarea{

border-radius:10px !important;

}

button{

border-radius:10px !important;

background:#0095f6 !important;

color:white !important;

}

</style>

""",unsafe_allow_html=True)

# ------------------------------------------
# Logo
# ------------------------------------------

st.markdown(
"<div class='logo'>Instagram</div>",
unsafe_allow_html=True
)

# ------------------------------------------
# Navigation
# ------------------------------------------

if st.session_state.logged_in:

    menu = st.sidebar.radio(

        "Menu",

        [

        "🏠 Home",

        "➕ Upload",

        "👤 Profile",

        "🔍 Search",

        "⚙ Settings",

        "🚪 Logout"

        ]

    )

else:

    menu = st.sidebar.radio(

        "Menu",

        [

        "Login",

        "Sign Up"

        ]

    )
    # ==========================================
# Part 2 - Login & Signup
# Continue below Part 1
# ==========================================

# -----------------------------
# Login Screen
# -----------------------------
if not st.session_state.logged_in and menu == "Login":

    st.markdown("## Welcome Back 👋")
    st.write("Login to your Instagram account")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_btn = st.button(
            "Login",
            use_container_width=True
        )

        if login_btn:

            if username == "" or password == "":

                st.warning(
                    "Please fill all fields."
                )

            else:

                user = login(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

    st.divider()

    st.info(
        "Don't have an account? Go to Sign Up."
    )

# -----------------------------
# Signup Screen
# -----------------------------
elif not st.session_state.logged_in and menu == "Sign Up":

    st.markdown("## Create New Account")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        fullname = st.text_input(
            "Full Name"
        )

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        create = st.button(
            "Create Account",
            use_container_width=True
        )

        if create:

            if (
                fullname == ""
                or username == ""
                or email == ""
                or password == ""
                or confirm == ""
            ):

                st.warning(
                    "Please fill all fields."
                )

            elif password != confirm:

                st.error(
                    "Passwords do not match."
                )

            elif user_exists(username):

                st.error(
                    "Username already exists."
                )

            else:

                try:

                    create_user(
                        username,
                        fullname,
                        email,
                        password
                    )

                    st.success(
                        "Account created successfully!"
                    )

                    st.balloons()

                except sqlite3.IntegrityError:

                    st.error(
                        "Email already registered."
                    )

# -----------------------------
# Logout
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "🚪 Logout"
):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.success(
        "Logged out successfully."
    )

    st.rerun()

# -----------------------------
# Placeholder Home
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "🏠 Home"
):

    st.title("🏠 Home Feed")

    st.success(
        f"Welcome @{st.session_state.username}"
    )

    st.write(
        "Feed will be added in Part 3."
    )

# -----------------------------
# Placeholder Upload
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "➕ Upload"
):

    st.title("Upload Post")

    st.info(
        "Upload feature coming in Part 3."
    )

# -----------------------------
# Placeholder Profile
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "👤 Profile"
):

    st.title("My Profile")

    cursor.execute(
        """
        SELECT fullname,
               email,
               bio,
               followers,
               following,
               joined
        FROM users
        WHERE username=?
        """,
        (
            st.session_state.username,
        )
    )

    user = cursor.fetchone()

    if user:

        st.subheader(user[0])

        st.write(
            "**Username:**",
            st.session_state.username
        )

        st.write(
            "**Email:**",
            user[1]
        )

        st.write(
            "**Bio:**",
            user[2]
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Followers",
            user[3]
        )

        c2.metric(
            "Following",
            user[4]
        )

        st.caption(
            "Joined : " + user[5]
        )

# -----------------------------
# Placeholder Search
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "🔍 Search"
):

    st.title("Search Users")

    keyword = st.text_input(
        "Search username"
    )

    if keyword:

        cursor.execute(
            """
            SELECT username,
                   fullname
            FROM users
            WHERE username LIKE ?
            """,
            (
                "%" + keyword + "%",
            )
        )

        users = cursor.fetchall()

        if users:

            for u in users:

                with st.container():

                    st.write(
                        "👤",
                        u[0]
                    )

                    st.caption(
                        u[1]
                    )

                    st.divider()

        else:

            st.warning(
                "No users found."
            )

# -----------------------------
# Placeholder Settings
# -----------------------------
elif (
    st.session_state.logged_in
    and menu == "⚙ Settings"
):

    st.title("Settings")

    st.info(
        "Settings page will be added later."
    )
