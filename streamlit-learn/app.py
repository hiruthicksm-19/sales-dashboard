# import streamlit as st
# st.title("Hello World")
# st.write("This is a simple Streamlit app.")
# name=st.text_input("Enter your name:")
# if name:
#     st.write(f"Hello, {name}!")

# if st.button("Click me!"):
#     st.write("Button clicked!")
# agree=st.checkbox("I agree")
# if agree:
#     st.write("You agreed!")
# selected=st.radio("Choose an option:", ("Option 1", "Option 2", "Option 3"))
# if selected:
#     st.write(f"You selected: {selected}")
# option = st.selectbox("Choose a number", [1, 2, 3, 4, 5])
# st.write("You chose:", option)

# age = st.slider("How old are you?", 0, 100, 25)
# st.write("Your age is", age)


import streamlit as st
import pandas as pd
import plotly.express as px
import io
# import plotly.express as px
# st.title("Display DataFrame")
# file=st.file_uploader("Upload a CSV file", type=["csv"])
# if file:
#     df=pd.read_csv(file)
#     st.success("File uploaded successfully!")
#     st.subheader("DataFrame")
#     st.dataframe(df)

#     st.subheader("Summary Stats")
#     st.write(df.describe())
    
#     st.subheader("🔢 Count of Price")
#     st.bar_chart(df['Price'].value_counts())

#     st.subheader("🌸 Price vs Total Sales")
#     fig = px.scatter(df, x="Price", y="Total Sales", color="Quantity", size="Quantity", hover_data=['Quantity'])
#     st.plotly_chart(fig)

st.set_page_config(page_title="Sales Dashboard",layout="wide")   
st.title("🛍️ Sales Dashboard")
uploaded_file = st.sidebar.file_uploader("📤 Upload your sales dataset (CSV)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Data Loaded!")

    

    # Show a preview
    st.subheader("📋 Data Preview")
    st.dataframe(df)


    st.sidebar.header("🔎 Filter Options")
    if "Category" in df.columns:
        categories = st.sidebar.multiselect(
            "Select Category:",
            options=df["Category"].unique(),
            default=df["Category"].unique()
        )
    else:
        categories = []
     # Payment Method Filter
    if "Payment Method" in df.columns:
        payment_methods = st.sidebar.multiselect(
            "Select Payment Method:",
            options=df["Payment Method"].unique(),
            default=df["Payment Method"].unique()
        )
    else:
        payment_methods = []

    # Apply filters
    df_filtered = df.copy()
    if categories:
        df_filtered = df_filtered[df_filtered["Category"].isin(categories)]
    if payment_methods:
        df_filtered = df_filtered[df_filtered["Payment Method"].isin(payment_methods)]

        # --- KPI Section ---
    st.subheader("📊 Key Performance Indicators")

    # Calculate KPIs
    total_sales = df_filtered["Total Sales"].sum() if "Total Sales" in df_filtered.columns else 0
    total_orders = df_filtered["Order ID"].nunique() if "Order ID" in df_filtered.columns else 0
    avg_order_value = total_sales / total_orders if total_orders else 0

    # Show KPIs in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📦 Total Orders", total_orders)
    col3.metric("💰 Avg. Order Value", f"${avg_order_value:,.2f}")

    # --- Visualizations ---
    st.subheader("📈 Visualizations")

    col1, col2 = st.columns(2)

    # Bar Chart: Sales by Category
    with col1:
        if "Category" in df_filtered.columns and "Total Sales" in df_filtered.columns:
            fig_bar = px.bar(
                df_filtered.groupby("Category", as_index=False).sum(),
                x="Category",
                y="Total Sales",
                color="Category",
                title="Sales by Category"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart: Payment Method Share
    with col2:
        if "Payment Method" in df_filtered.columns and "Total Sales" in df_filtered.columns:
            fig_pie = px.pie(
                df_filtered,
                names="Payment Method",
                values="Total Sales",
                title="Payment Method Share"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter Plot: Price vs Total Sales
    st.subheader("💡 Price vs Total Sales")
    if {"Price", "Total Sales", "Category", "Quantity"}.issubset(df_filtered.columns):
        fig_scatter = px.scatter(
            df_filtered,
            x="Price",
            y="Total Sales",
            color="Category",
            size="Quantity",
            hover_data=["Product"],
            title="Price vs Total Sales (by Category)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Display filtered data
    st.subheader("📋 Filtered Data Preview")
    st.dataframe(df_filtered)

    st.markdown("---")
    st.subheader("⬇️ Download Filtered Data")

    if not df_filtered.empty:
        # Convert to CSV and encode
        csv = df_filtered.to_csv(index=False)
        csv_bytes = csv.encode('utf-8')

        # Create a download button
        st.download_button(
            label="📥 Download CSV",
            data=csv_bytes,
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No data to download. Try adjusting your filters.")
           
else:
    st.info("👈 Upload a CSV file from the sidebar to get started.")


