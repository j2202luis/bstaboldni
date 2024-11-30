import streamlit as st

# Dummy database of usernames and passwords
users_db = {
    "user1": "password123",
    "user2": "mypassword",
    "admin": "adminpass"
}

# Function for login page
def login():
    st.title("Login Page")
    st.write("Please enter your username and password to log in.")

    # Get user input for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check for login
    if st.button("Login"):
        if username in users_db and users_db[username] == password:
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password. Please try again.")
            return False
    return False

# Main app
def main():
    if login():
        st.write("Welcome to the main app!")
        st.write("You are now logged in.")
        # Place your main app content here
    else:
        st.write("Please log in to continue.")

if __name__ == "__main__":
    main()
