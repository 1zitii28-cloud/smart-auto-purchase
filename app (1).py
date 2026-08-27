
import streamlit as st
import pandas as pd

# ==========================================
# 網頁設定
# ==========================================

st.set_page_config(
    page_title="智慧自動採購系統",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# 標題
# ==========================================

st.title("📦 智慧自動採購系統")
st.caption("Smart Auto Purchase System")

st.write(
    "系統會根據目前庫存與安全庫存，自動計算需要補充的商品數量，"
    "並在確認後啟動自動採購流程。"
)

st.divider()


# ==========================================
# 建立模擬倉庫資料
# ==========================================

warehouse = [
    {
        "sku": "ITEM-001",
        "product_name": "Box of Chocolate",
        "local_stock": 2,
        "target_stock": 10,
        "store_url": "https://web-scraping.dev/product/1"
    },
    {
        "sku": "ITEM-002",
        "product_name": "Orange Juice",
        "local_stock": 8,
        "target_stock": 10,
        "store_url": "https://web-scraping.dev/product/2"
    },
    {
        "sku": "ITEM-003",
        "product_name": "Energy Drink",
        "local_stock": 15,
        "target_stock": 10,
        "store_url": "https://web-scraping.dev/product/3"
    }
]


# ==========================================
# 計算庫存狀態
# ==========================================

for item in warehouse:

    shortage = (
        item["target_stock"]
        - item["local_stock"]
    )

    if shortage > 0:
        item["needed_qty"] = shortage
        item["status"] = "庫存不足"
    else:
        item["needed_qty"] = 0
        item["status"] = "庫存充足"


# ==========================================
# Dashboard 統計
# ==========================================

total_products = len(warehouse)

low_stock_products = sum(
    1
    for item in warehouse
    if item["needed_qty"] > 0
)

total_needed = sum(
    item["needed_qty"]
    for item in warehouse
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📦 商品總數",
        total_products
    )

with col2:

    st.metric(
        "⚠️ 庫存不足商品",
        low_stock_products
    )

with col3:

    st.metric(
        "🛒 待採購數量",
        total_needed
    )


st.divider()


# ==========================================
# 庫存表
# ==========================================

st.subheader("📊 庫存狀態")

table_data = []

for item in warehouse:

    table_data.append({

        "SKU": item["sku"],

        "商品名稱":
        item["product_name"],

        "目前庫存":
        item["local_stock"],

        "安全庫存":
        item["target_stock"],

        "需要採購":
        item["needed_qty"],

        "狀態":
        item["status"]
    })


df = pd.DataFrame(table_data)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================
# 自動採購區域
# ==========================================

st.subheader("🤖 自動採購")

if total_needed > 0:

    st.warning(
        f"目前有 {low_stock_products} 項商品庫存不足，"
        f"總共需要採購 {total_needed} 件。"
    )

else:

    st.success(
        "目前所有商品庫存充足，不需要採購。"
    )


# ==========================================
# 開始採購按鈕
# ==========================================

if st.button(
    "🚀 開始自動採購",
    type="primary",
    use_container_width=True
):

    st.session_state["purchase_started"] = True


# ==========================================
# 採購流程顯示
# ==========================================

if st.session_state.get(
    "purchase_started",
    False
):

    st.divider()

    st.subheader(
        "⚙️ 自動採購執行紀錄"
    )

    progress = st.progress(0)

    status_box = st.empty()

    status_box.info(
        "🔄 正在分析倉庫庫存..."
    )

    progress.progress(20)

    status_box.info(
        "✓ 庫存分析完成"
    )

    progress.progress(40)

    status_box.info(
        "🔐 準備登入採購平台..."
    )

    progress.progress(60)

    status_box.info(
        "🛒 準備加入缺貨商品..."
    )

    progress.progress(80)

    status_box.info(
        "🔎 準備驗證購物車..."
    )

    progress.progress(100)

    status_box.success(
        "✓ 自動採購流程準備完成"
    )


    st.subheader(
        "📋 本次採購需求"
    )

    purchase_data = []

    for item in warehouse:

        if item["needed_qty"] > 0:

            purchase_data.append({

                "商品名稱":
                item["product_name"],

                "目前庫存":
                item["local_stock"],

                "安全庫存":
                item["target_stock"],

                "採購數量":
                item["needed_qty"],

                "狀態":
                "待執行"
            })


    purchase_df = pd.DataFrame(
        purchase_data
    )

    st.dataframe(
        purchase_df,
        use_container_width=True,
        hide_index=True
    )


    st.info(
        "🛑 為了避免實際付款，本系統的自動化流程將停止在購物車驗證階段。"
    )
