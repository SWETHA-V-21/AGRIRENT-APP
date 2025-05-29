import streamlit as st

# Initialize session state for equipments and bookings
if 'equipments' not in st.session_state:
    st.session_state.equipments = []

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

st.title("AgriRent: AI-Enabled Equipment Sharing Platform")
tabs = st.tabs(["Seller", "Buyer"])

# Seller Tab
with tabs[0]:
    st.header("🚜 Seller Portal")
    st.subheader("Add Your Equipment")

    with st.form("Add Equipment"):
        name = st.text_input("Equipment Name")
        description = st.text_area("Description")
        price = st.number_input("Rental Price per Day (in ₹)", min_value=0)
        image_url = st.text_input("Image URL (optional)")
        submit = st.form_submit_button("Add Equipment")

        if submit and name and description and price:
            st.session_state.equipments.append({
                "name": name,
                "description": description,
                "price": price,
                "image_url": image_url,
                "booked_by": None
            })
            st.success(f"✅ '{name}' added successfully!")

    st.subheader("Your Listed Equipments")
    for i, eq in enumerate(st.session_state.equipments):
        with st.expander(f"{eq['name']} - ₹{eq['price']}/day"):
            st.write(eq['description'])
            if eq['image_url']:
                st.image(eq['image_url'], use_column_width=True)
            st.write(f"Booked By: {eq['booked_by'] if eq['booked_by'] else 'Not Booked'}")
            if st.button("Delete", key=f"del{i}"):
                st.session_state.equipments.pop(i)
                st.rerun()

    st.subheader("Bookings on Your Equipment")
    seller_bookings = [b for b in st.session_state.bookings if b['equipment'] in [e['name'] for e in st.session_state.equipments]]
    if seller_bookings:
        for b in seller_bookings:
            st.write(f"🔔 {b['buyer_name']} booked '{b['equipment']}' for ₹{b['price']}/day")
    else:
        st.info("No bookings yet.")

# Buyer Tab
with tabs[1]:
    st.header("🧑‍🌾 Buyer Portal")
    st.subheader("Available Equipments")

    for i, eq in enumerate(st.session_state.equipments):
        if not eq['booked_by']:
            with st.expander(f"{eq['name']} - ₹{eq['price']}/day"):
                st.write(eq['description'])
                if eq['image_url']:
                    st.image(eq['image_url'], use_column_width=True)
                with st.form(f"book{i}"):
                    buyer_name = st.text_input("Your Name", key=f"name{i}")
                    confirm = st.form_submit_button("Book Now")
                    if confirm and buyer_name:
                        eq['booked_by'] = buyer_name
                        st.session_state.bookings.append({
                            "equipment": eq['name'],
                            "price": eq['price'],
                            "buyer_name": buyer_name
                        })
                        st.success(f"🎉 Congratulations {buyer_name}, you booked '{eq['name']}'!")
                        st.markdown(f"**📃 Rental Bill**\n\n- Equipment: {eq['name']}\n- Price: ₹{eq['price']} per day\n- Rentee: {buyer_name}")
                        st.rerun()
