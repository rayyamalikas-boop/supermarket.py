import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 Business Dashboard – Excel Data Analyzer")

# --- UPLOAD FILE ---
uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Preview Data")
    st.dataframe(df.head())

    st.markdown("---")

    # Pastikan kolom penting ada
    required_columns = ["Tanggal", "Kategori", "Nilai", "Kuantitas"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"File harus memiliki kolom: {required_columns}")
    else:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])

        # === 1. Bar Chart: Total Nilai per Kategori ===
        st.subheader("1️⃣ Total Nilai per Kategori")
        total_by_cat = df.groupby("Kategori")["Nilai"].sum()
        st.bar_chart(total_by_cat)

        # === 2. Line Chart: Tren Nilai per Tanggal ===
        st.subheader("2️⃣ Tren Nilai dari Waktu ke Waktu")
        trend = df.groupby("Tanggal")["Nilai"].sum()
        st.line_chart(trend)

        # === 3. Pie Chart: Distribusi Kategori ===
        st.subheader("3️⃣ Distribusi Nilai per Kategori (Pie Chart)")
        fig1, ax1 = plt.subplots()
        ax1.pie(total_by_cat, labels=total_by_cat.index, autopct="%1.1f%%")
        ax1.axis("equal")
        st.pyplot(fig1)

        # === 4. Histogram: Distribusi Nilai ===
        st.subheader("4️⃣ Histogram Distribusi Nilai")
        fig2, ax2 = plt.subplots()
        ax2.hist(df["Nilai"], bins=10)
        ax2.set_xlabel("Nilai")
        ax2.set_ylabel("Frekuensi")
        st.pyplot(fig2)

        # === 5. Scatter Plot: Nilai vs Kuantitas ===
        st.subheader("5️⃣ Scatter Plot – Nilai vs Kuantitas")
        fig3, ax3 = plt.subplots()
        ax3.scatter(df["Kuantitas"], df["Nilai"])
        ax3.set_xlabel("Kuantitas")
        ax3.set_ylabel("Nilai")
        st.pyplot(fig3)

else:
    st.info("Silakan upload file Excel untuk memulai analisis.")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===== PAGE SETUP =====
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ===== CSS CUSTOM STYLE (WARNA PERSIS SEPERTI EXCEL) =====
st.markdown("""
    <style>
        .title-box {
            background-color: #e34a87;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 40px;
            font-weight: bold;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .kpi-card {
            padding: 20px;
            background-color: #f7f2d7;
            border: 3px solid #e3b300;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        .kpi-value {
            font-size: 30px;
            color: #8d0045;
            font-weight: bold;
        }
        .sidebar-box {
            background-color: #f1cd60;
            padding: 20px;
            border-radius: 10px;
            color: black;
            font-weight: bold;
            font-size: 17px;
        }
    </style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="title-box">SALES DASHBOARD</div>', unsafe_allow_html=True)

# ===== LAYOUT =====
left_sidebar, main_area = st.columns([1, 4])

# ================================
#      LEFT SIDEBAR (FILTER)
# ================================
with left_sidebar:

    st.markdown("""
        <div class="sidebar-box">
            <h3 style="text-align:center;">GROUP 1</h3>
            <p>Ulfie Aulia (014202500194)</p>
            <p>Lidya Khoirun Nisa (014202500168)</p>
            <p>Rayya Malika Subiyantoro (014202500161)</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 🔍 Filters")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df["Date"] = pd.to_datetime(df["Date"])

        # Filters
        city = st.multiselect("City", df["City"].unique(), default=df["City"].unique())
        customer = st.multiselect("Customer Type", df["Customer type"].unique(), default=df["Customer type"].unique())
        product = st.multiselect("Product Line", df["Product line"].unique(), default=df["Product line"].unique())
        payment = st.multiselect("Payment", df["Payment"].unique(), default=df["Payment"].unique())

        df = df[
            (df["City"].isin(city)) &
            (df["Customer type"].isin(customer)) &
            (df["Product line"].isin(product)) &
            (df["Payment"].isin(payment))
        ]


# ================================
#           MAIN AREA
# ================================
if uploaded_file:

    # ===== KPI CARDS =====
    k1, k2, k3, k4 = main_area.columns(4)

    total_sales = df["Total"].sum()
    products_sold = df["Quantity"].sum()
    cogs = df["cogs"].sum()
    avg_rating = df["Rating"].mean()

    with k1:
        st.markdown('<div class="kpi-card">TOTAL SALES<br><span class="kpi-value">${:,.0f}</span></div>'.format(total_sales), unsafe_allow_html=True)

    with k2:
        st.markdown('<div class="kpi-card">NUMBER OF PRODUCT SOLD<br><span class="kpi-value">{}</span></div>'.format(products_sold), unsafe_allow_html=True)

    with k3:
        st.markdown('<div class="kpi-card">COST OF GOODS SOLD<br><span class="kpi-value">${:,.0f}</span></div>'.format(cogs), unsafe_allow_html=True)

    with k4:
        st.markdown('<div class="kpi-card">AVERAGE RATING<br><span class="kpi-value">{:.2f}</span></div>'.format(avg_rating), unsafe_allow_html=True)

    st.write("---")

    # ===== CHART ROW 1 =====
    c1, c2 = main_area.columns(2)

    # Monthly Sales Line Chart
    with c1:
        st.subheader("📈 MONTHLY SALES")
        monthly = df.groupby(df["Date"].dt.month)["Total"].sum()
        st.line_chart(monthly)

    # Payment Method Pie Chart
    with c2:
        st.subheader("💳 PAYMENT METHOD")
        payment_count = df["Payment"].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.pie(payment_count, labels=payment_count.index, autopct="%1.1f%%")
        ax1.axis("equal")
        st.pyplot(fig1)

    # ===== CHART ROW 2 =====
    d1, d2 = main_area.columns(2)

    # Product Sold
    with d1:
        st.subheader("📦 PRODUCT SOLD")
        product_sales = df.groupby("Product line")["Quantity"].sum()
        st.bar_chart(product_sales)

    # Rating by City
    with d2:
        st.subheader("⭐ RATING BY CITY")
        rating_city = df.groupby("City")["Rating"].mean()
        st.bar_chart(rating_city)

else:
    main_area.info("Silakan upload file Excel untuk menampilkan dashboard.")
