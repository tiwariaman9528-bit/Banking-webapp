import streamlit as st
from bank import Bank

st.set_page_config(page_title="StreamBank App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

# Initialize session state for authentication
if 'user' not in st.session_state:
    st.session_state.user = None

def login():
    st.session_state.user = None

def logout():
    st.session_state.user = None
    st.success("Logged out successfully!")

# Sidebar Navigation
if st.session_state.user:
    st.sidebar.success(f"Logged in as: {st.session_state.user['name']}")
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Deposit", "Withdraw", "Update Info", "Delete Account"]
    )
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
else:
    menu = st.sidebar.selectbox("Menu", ["Login", "Create Account"])

# Page Logic
if menu == "Create Account":
    st.subheader("👤 Create New Account")
    with st.form("create_account_form"):
        name = st.text_input("Your Name")
        age = st.number_input("Your Age", min_value=0, step=1)
        email = st.text_input("Your Email")
        pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Create Account")

    if submit:
        if name and email and pin:
            try:
                user, msg = Bank.create_account(name, int(age), email, int(pin))
                if user:
                    st.success(msg)
                    st.info(f"Your Account Number: {user['accountNo.']}")
                    st.session_state.user = user  # Auto-login after creation
                    st.markdown("Please **Login** specifically if auto-redirect doesn't work (or just refresh).")
                    st.rerun()
                else:
                    st.error(msg)
            except ValueError:
                st.error("Invalid input. Please check your details.")
        else:
            st.warning("All fields are required.")

elif menu == "Login":
    st.subheader("🔐 Login to Your Account")
    with st.form("login_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Login")
    
    if submit:
        if acc_no and pin:
            try:
                user = Bank.find_user(acc_no, int(pin))
                if user:
                    st.session_state.user = user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Account Number or PIN.")
            except ValueError:
                st.error("PIN must be numeric.")
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "Dashboard":
    if st.session_state.user:
        user = st.session_state.user
        st.subheader("📊 Your Dashboard")
        st.info(f"**Account Number:** {user['accountNo.']}")
        st.info(f"**Name:** {user['name']}")
        
        # Refresh user data to get latest balance
        # Note: Bank.find_user requires PIN. We have it in session.
        # Ideally we shouldn't store PIN in session for real security, but for this simpler app model it's necessary unless we refactor to token/session logic in backend.
        # Story S3 says: "Store authenticated user details in st.session_state".
        updated_user = Bank.find_user(user['accountNo.'], user['pin'])
        if updated_user:
            st.session_state.user = updated_user # Update session
            st.metric(label="Current Balance", value=f"₹ {updated_user['balance']}")
        else:
            st.error("Error fetching latest data.")

elif menu == "Deposit":
    st.subheader("💰 Deposit Money")
    if st.session_state.user:
        user = st.session_state.user
        st.write(f"Depositing to Account: **{user['accountNo.']}**")
        amount = st.number_input("Amount to Deposit", min_value=1)
        
        if st.button("Deposit"):
            success, msg = Bank.deposit(user['accountNo.'], user['pin'], int(amount))
            if success:
                st.success(msg)
                # Refresh session
                updated_user = Bank.find_user(user['accountNo.'], user['pin'])
                if updated_user:
                    st.session_state.user = updated_user
            else:
                st.error(msg)

elif menu == "Withdraw":
    st.subheader("🏧 Withdraw Money")
    if st.session_state.user:
        user = st.session_state.user
        st.write(f"Withdrawing from Account: **{user['accountNo.']}**")
        st.info(f"Current Balance: ₹ {user['balance']}")
        amount = st.number_input("Amount to Withdraw", min_value=1)
        
        if st.button("Withdraw"):
            success, msg = Bank.withdraw(user['accountNo.'], user['pin'], int(amount))
            if success:
                st.success(msg)
                updated_user = Bank.find_user(user['accountNo.'], user['pin'])
                if updated_user:
                    st.session_state.user = updated_user
            else:
                st.error(msg)

elif menu == "Update Info":
    st.subheader("✏️ Update Profile")
    st.info("Feature currently under maintenance.")

elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    st.info("Feature currently under maintenance.")
