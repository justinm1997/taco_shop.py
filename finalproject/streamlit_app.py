"""
TACO SHOP STREAMLIT APP
Based on tacoshop2.py
Features: CRUD operations with text file persistence
Developer: Justin Moravec
"""

import streamlit as st
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================
MENU_FILE = "menu.txt"
ORDER_FILE = "order_history.txt"
TORTILLA_OPTIONS = ("Corn", "Flour")
MEAT_OPTIONS = ("Chicken", "Beef", "Steak")
TOPPING_OPTIONS = ("Lettuce", "Cilantro", "Tomato", "Cheese", "Onion", "Salsa")
CATEGORY_OPTIONS = ("Taco", "Burrito", "Nachos")

# Pricing
CATEGORY_PRICES = {"Taco": 3.00, "Burrito": 8.00, "Nachos": 10.00}
PROTEIN_UPCHARGE = {"Beef": 1.00, "Chicken": 1.00, "Steak": 2.00}
EXTRA_COST = 0.25

# Set page config
st.set_page_config(
    page_title="🌮 Taco Shop", layout="wide", initial_sidebar_state="expanded"
)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def calculate_total(category, protein, extras_count):
    """Calculate order total based on selections."""
    base = CATEGORY_PRICES.get(category, 3.00)
    protein_cost = PROTEIN_UPCHARGE.get(protein, 0)
    extras_total = extras_count * EXTRA_COST
    return base + protein_cost + extras_total


def save_order(customer_name, table_number, category, tortilla, protein, extras, total):
    """Save order to order_history.txt with timestamp"""
    extras_str = "|".join(extras) if extras else "None"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ORDER_FILE, "a") as f:
        f.write(
            f"{timestamp},{customer_name},{table_number},{category},{tortilla},{protein},{extras_str},{total:.2f}\n"
        )


def read_all_orders():
    """Read all orders from order_history.txt"""
    if not os.path.exists(ORDER_FILE):
        return []

    orders = []
    with open(ORDER_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) >= 8:
                    orders.append(
                        {
                            "timestamp": parts[0],
                            "customer": parts[1],
                            "table": parts[2],
                            "category": parts[3],
                            "tortilla": parts[4],
                            "protein": parts[5],
                            "extras": parts[6],
                            "total": parts[7],
                            "raw": line,
                        }
                    )
    return orders


def delete_order(order_index):
    """Delete an order by index"""
    orders = read_all_orders()
    if 0 <= order_index < len(orders):
        orders.pop(order_index)
        with open(ORDER_FILE, "w") as f:
            for order in orders:
                f.write(order["raw"] + "\n")
        return True
    return False


def update_order(
    order_index,
    new_customer,
    new_table,
    new_category,
    new_tortilla,
    new_protein,
    new_extras,
    new_total,
):
    """Update all fields of an order (preserves original timestamp)"""
    orders = read_all_orders()
    if 0 <= order_index < len(orders):
        order = orders[order_index]
        extras_str = "|".join(new_extras) if new_extras else "None"
        updated_line = f"{order['timestamp']},{new_customer},{new_table},{new_category},{new_tortilla},{new_protein},{extras_str},{new_total:.2f}"
        orders[order_index]["raw"] = updated_line

        with open(ORDER_FILE, "w") as f:
            for o in orders:
                f.write(o["raw"] + "\n")
        return True
    return False


# ============================================================================
# PAGE: CREATE ORDER
# ============================================================================


def page_create_order():
    st.header("🛒 Create New Order")

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter name").title()
        table_number = st.text_input("Table Number", placeholder="Enter table number")

    with col2:
        st.write("")  # Spacing
        st.write("")

    st.divider()

    # Category selection
    category = st.radio("📋 Category", CATEGORY_OPTIONS, horizontal=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Tortilla (only for Taco)
        if category == "Taco":
            tortilla = st.selectbox("🌯 Tortilla Type", TORTILLA_OPTIONS)
        else:
            tortilla = "N/A"
            st.info(f"ℹ️ Tortilla N/A for {category}")

    with col2:
        # Protein
        protein = st.selectbox("🍗 Protein", MEAT_OPTIONS)

    with col3:
        st.write("")  # Spacing

    # Extras (multi-select)
    st.write("**🥬 Extras** (select as many as you want)")
    extras = st.multiselect(
        "Select toppings", TOPPING_OPTIONS, default=[], label_visibility="collapsed"
    )

    st.divider()

    # Price calculation and display
    total = calculate_total(category, protein, len(extras))

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.metric("💰 Total", f"${total:.2f}")

    st.divider()

    # Submit button
    if st.button("✅ Confirm Order", use_container_width=True, type="primary"):
        # Validation
        if not customer_name:
            st.error("❌ Please enter a customer name")
        elif not table_number:
            st.error("❌ Please enter a table number")
        elif not table_number.isdigit():
            st.error("❌ Table number must be numeric")
        else:
            save_order(
                customer_name, table_number, category, tortilla, protein, extras, total
            )
            st.success(f"✅ Order saved! Total: ${total:.2f}")
            st.balloons()


# ============================================================================
# PAGE: READ ORDERS
# ============================================================================


def page_read_orders():
    st.header("📖 View All Orders")

    orders = read_all_orders()

    if not orders:
        st.info("📭 No orders found")
        return

    st.write(f"**Total Orders: {len(orders)}**")
    st.divider()

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        filter_by = st.radio(
            "Filter by:",
            ["All Orders", "Customer Name", "Table Number"],
            horizontal=True,
        )

    filtered_orders = orders

    if filter_by == "Customer Name":
        search_name = st.text_input("Enter customer name to search").title()
        if search_name:
            filtered_orders = [
                o for o in orders if search_name.lower() in o["customer"].lower()
            ]

    elif filter_by == "Table Number":
        search_table = st.text_input("Enter table number to search")
        if search_table:
            filtered_orders = [o for o in orders if search_table in o["table"]]

    st.divider()

    # Display orders
    for idx, order in enumerate(filtered_orders):
        with st.expander(
            f"📦 Order #{idx+1} - {order['customer']} (Table {order['table']})"
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Customer:** {order['customer']}")
                st.write(f"**Table:** {order['table']}")
                st.write(f"**Category:** {order['category']}")

            with col2:
                st.write(f"**Tortilla:** {order['tortilla']}")
                st.write(f"**Protein:** {order['protein']}")
                st.write(f"**Extras:** {order['extras']}")

            st.write(f"**⏰ Order Time:** {order['timestamp']}")
            st.write(f"**💰 Total:** ${order['total']}")


# ============================================================================
# PAGE: UPDATE ORDER
# ============================================================================


def page_update_order():
    st.header("✏️ Update Order")

    orders = read_all_orders()

    if not orders:
        st.info("📭 No orders to update")
        return

    # Select order to update
    order_options = [
        f"{idx}: {o['customer']} (Table {o['table']}) - ${o['total']}"
        for idx, o in enumerate(orders)
    ]
    selected_order = st.selectbox(
        "Select order to update",
        range(len(orders)),
        format_func=lambda x: order_options[x],
    )

    st.divider()

    current_order = orders[selected_order]
    extras_list = [e for e in current_order["extras"].split("|") if e != "None"]

    st.write("**Current Order Details:**")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Customer: {current_order['customer']}")
        st.write(f"Category: {current_order['category']}")
        st.write(f"Protein: {current_order['protein']}")

    with col2:
        st.write(f"Table: {current_order['table']}")
        st.write(f"Tortilla: {current_order['tortilla']}")
        st.write(f"Extras: {current_order['extras']}")

    st.write(f"**⏰ Order Time:** {current_order['timestamp']}")

    st.divider()

    st.write("**Update Fields:**")
    col1, col2 = st.columns(2)

    with col1:
        new_customer = st.text_input(
            "Customer Name", value=current_order["customer"]
        ).title()
        new_table = st.text_input("Table Number", value=current_order["table"])

    with col2:
        new_category = st.selectbox(
            "Category",
            CATEGORY_OPTIONS,
            index=list(CATEGORY_OPTIONS).index(current_order["category"]),
        )

    st.divider()

    # Conditional tortilla field
    col1, col2, col3 = st.columns(3)

    with col1:
        if new_category == "Taco":
            new_tortilla = st.selectbox(
                "Tortilla Type",
                TORTILLA_OPTIONS,
                index=(
                    list(TORTILLA_OPTIONS).index(current_order["tortilla"])
                    if current_order["tortilla"] != "N/A"
                    else 0
                ),
            )
        else:
            new_tortilla = "N/A"
            st.info(f"ℹ️ Tortilla N/A for {new_category}")

    with col2:
        new_protein = st.selectbox(
            "Protein",
            MEAT_OPTIONS,
            index=list(MEAT_OPTIONS).index(current_order["protein"]),
        )

    with col3:
        st.write("")  # Spacing

    st.divider()

    st.write("**Extras:**")
    new_extras = st.multiselect(
        "Select toppings",
        TOPPING_OPTIONS,
        default=extras_list,
        label_visibility="collapsed",
    )

    st.divider()

    # Recalculate total
    new_total = calculate_total(new_category, new_protein, len(new_extras))

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.metric("💰 New Total", f"${new_total:.2f}")

    st.divider()

    if st.button("💾 Save Changes", use_container_width=True, type="primary"):
        if not new_customer:
            st.error("❌ Customer name cannot be empty")
        elif not new_table:
            st.error("❌ Table number cannot be empty")
        elif not new_table.isdigit():
            st.error("❌ Table number must be numeric")
        else:
            if update_order(
                selected_order,
                new_customer,
                new_table,
                new_category,
                new_tortilla,
                new_protein,
                new_extras,
                new_total,
            ):
                st.success("✅ Order updated successfully!")
            else:
                st.error("❌ Failed to update order")


# ============================================================================
# PAGE: DELETE ORDER
# ============================================================================


def page_delete_order():
    st.header("🗑️ Delete Order")

    orders = read_all_orders()

    if not orders:
        st.info("📭 No orders to delete")
        return

    # Select order to delete
    order_options = [
        f"{idx}: {o['customer']} (Table {o['table']}) - ${o['total']}"
        for idx, o in enumerate(orders)
    ]
    selected_order = st.selectbox(
        "Select order to delete",
        range(len(orders)),
        format_func=lambda x: order_options[x],
    )

    st.divider()

    current_order = orders[selected_order]

    st.warning("⚠️ **This action cannot be undone!**")

    st.write("**Order to be deleted:**")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Customer: {current_order['customer']}")
        st.write(f"Category: {current_order['category']}")

    with col2:
        st.write(f"Table: {current_order['table']}")
        st.write(f"Total: ${current_order['total']}")

    st.write(f"**⏰ Order Time:** {current_order['timestamp']}")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        pass

    with col2:
        if st.button("🗑️ Delete Order", use_container_width=True, type="secondary"):
            if delete_order(selected_order):
                st.success("✅ Order deleted successfully!")
            else:
                st.error("❌ Failed to delete order")

    with col3:
        pass


# ============================================================================
# MAIN APP
# ============================================================================


def main():
    # Sidebar navigation
    st.sidebar.title("🌮 TACO SHOP")
    st.sidebar.write("---")

    page = st.sidebar.radio(
        "Navigation",
        ["➕ Create Order", "📖 View Orders", "✏️ Update Order", "🗑️ Delete Order"],
        label_visibility="collapsed",
    )

    st.sidebar.write("---")
    st.sidebar.info(
        "📝 **CRUD Operations System**\n\nManage taco shop orders with full Create, Read, Update, Delete functionality!"
    )

    # Route to appropriate page
    if page == "➕ Create Order":
        page_create_order()
    elif page == "📖 View Orders":
        page_read_orders()
    elif page == "✏️ Update Order":
        page_update_order()
    elif page == "🗑️ Delete Order":
        page_delete_order()


if __name__ == "__main__":
    main()
