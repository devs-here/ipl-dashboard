from abc import ABC, abstractmethod
import streamlit as st

# ───────────────────────────── Core Classes ─────────────────────────────

class LibraryItem(ABC):
    def __init__(self, title, id, available=True):
        self.title = title
        self.id = id
        self.__available = available
        self.borrowed_by = None

    @abstractmethod
    def get_details(self):
        pass

    def borrow(self, user):
        if self.__available:
            self.__available = False
            self.borrowed_by = user

    def return_item(self):
        self.__available = True
        self.borrowed_by = None

    def is_available(self):
        return self.__available


class Book(LibraryItem):
    def __init__(self, title, id):
        super().__init__(title, id)

    def get_details(self):
        status = "Available" if self.is_available() else "Not Available"
        return f"📘 Book: {self.title} | ID: {self.id} | {status}"


class Magazine(LibraryItem):
    def __init__(self, title, id):
        super().__init__(title, id)

    def get_details(self):
        status = "Available" if self.is_available() else "Not Available"
        return f"📰 Magazine: {self.title} | ID: {self.id} | {status}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_items = []

    def borrow_item(self, item):
        self.borrowed_items.append(item)

    def return_item(self, item):
        self.borrowed_items.remove(item)


class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def lend_item(self, user, item):
        if item.is_available():
            item.borrow(user)
            user.borrow_item(item)
            return True, f"✅ '{item.title}' borrowed by {user.name}."
        else:
            return False, f"❌ '{item.title}' is already borrowed by {item.borrowed_by.name}."

    def accept_return(self, user, item):
        if item in user.borrowed_items:
            item.return_item()
            user.return_item(item)
            return True, f"✅ '{item.title}' returned by {user.name}."
        else:
            return False, f"❌ {user.name} did not borrow '{item.title}'."


# ───────────────────────────── Login System ──────────────────────────────

# Add or change users here — "username": "password"

def show_login():
    st.title("📚 Library Management System")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            accounts = st.session_state.accounts
            if username.lower() in accounts and accounts[username.lower()] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username.lower()
                st.rerun()
            else:
                st.error("❌ Wrong username or password.")

    with tab_register:
        new_username = st.text_input("Choose username", key="reg_user")
        new_password = st.text_input("Choose password", type="password", key="reg_pass")
        if st.button("Register"):
            if not new_username.strip() or not new_password.strip():
                st.error("Fill in both fields.")
            elif new_username.lower() in st.session_state.accounts:
                st.error("❌ Username already taken.")
            else:
                st.session_state.accounts[new_username.lower()] = new_password
                st.success(f"✅ Account created! You can now login as '{new_username}'.")

def show_logout():
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("📚 Library Management System")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()


# ───────────────────────── Session State Setup ───────────────────────────

def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None

    if "accounts" not in st.session_state:
        st.session_state.accounts = {}

    if "library" not in st.session_state:
        lib = Library()
        st.session_state.library = lib

    if "users" not in st.session_state:
        st.session_state.users = []


# ───────────────────────────── Streamlit UI ──────────────────────────────

init_state()

if not st.session_state.logged_in:
        show_login()
        st.stop()

show_logout()
if st.session_state.current_user:
    st.write(f"👋 Welcome, **{st.session_state.current_user.capitalize()}**!")

lib: Library = st.session_state.library
users: list[User] = st.session_state.users

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Catalog", "Borrow", "Return", "Users", "Add Items"])

# ── Tab 1: Catalog ──
with tab1:
    st.subheader("All Library Items")
    if not lib.items:
        st.info("No items in the library yet.")
    for item in lib.items:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(item.get_details())
        with col2:
            if item.is_available():
                st.success("Free")
            else:
                st.error(f"Taken by {item.borrowed_by.name}")

# ── Tab 2: Borrow ──
with tab2:
    st.subheader("Borrow an Item")

    user_names = [u.name for u in users]
    available_items = [i for i in lib.items if i.is_available()]

    if not users:
        st.warning("No users added yet. Go to the Users tab.")
    elif not available_items:
        st.warning("No items available to borrow right now.")
    else:
        selected_user = st.selectbox("Select user", user_names, key="borrow_user")
        selected_item_title = st.selectbox(
            "Select item",
            [f"{i.title} (ID: {i.id})" for i in available_items],
            key="borrow_item"
        )

        if st.button("Borrow"):
            user = next(u for u in users if u.name == selected_user)
            item = available_items[[f"{i.title} (ID: {i.id})" for i in available_items].index(selected_item_title)]
            success, msg = lib.lend_item(user, item)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# ── Tab 3: Return ──
with tab3:
    st.subheader("Return an Item")

    users_with_items = [u for u in users if u.borrowed_items]

    if not users_with_items:
        st.info("Nobody has borrowed anything right now.")
    else:
        selected_user_name = st.selectbox("Select user", [u.name for u in users_with_items], key="return_user")
        user = next(u for u in users if u.name == selected_user_name)

        item_titles = [f"{i.title} (ID: {i.id})" for i in user.borrowed_items]
        selected_item_title = st.selectbox("Select item to return", item_titles, key="return_item")

        if st.button("Return"):
            item = user.borrowed_items[item_titles.index(selected_item_title)]
            success, msg = lib.accept_return(user, item)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# ── Tab 4: Users ──
with tab4:
    st.subheader("Add New User")
    new_name = st.text_input("User name", placeholder="e.g. Rahul", key="new_user")
    if st.button("Add User"):
        if not new_name.strip():
            st.error("Please enter a name.")
        elif any(u.name.lower() == new_name.strip().lower() for u in users):
            st.error(f"'{new_name}' already exists.")
        else:
            users.append(User(new_name.strip()))
            st.success(f"User '{new_name.strip()}' added!")

    st.divider()
    st.subheader("All Users")
    if not users:
        st.info("No users yet.")
    for u in users:
        if u.borrowed_items:
            items_str = ", ".join(i.title for i in u.borrowed_items)
            st.write(f"**{u.name}** — borrowed: {items_str}")
        else:
            st.write(f"**{u.name}** — nothing borrowed")

# ── Tab 5: Add Items ──
with tab5:
    st.subheader("Add a New Book or Magazine")
    item_type = st.selectbox("Type", ["Book", "Magazine"], key="new_item_type")
    new_title = st.text_input("Title", placeholder="e.g. The Alchemist", key="new_title")
    new_id = st.number_input("ID", min_value=1, step=1, key="new_id")

    if st.button("Add Item"):
        if not new_title.strip():
            st.error("Please enter a title.")
        elif any(i.id == int(new_id) for i in lib.items):
            st.error(f"ID {int(new_id)} already exists.")
        else:
            new_item = Book(new_title.strip(), int(new_id)) if item_type == "Book" else Magazine(new_title.strip(), int(new_id))
            lib.add_item(new_item)
            st.success(f"{item_type} '{new_title.strip()}' added with ID {int(new_id)}!")