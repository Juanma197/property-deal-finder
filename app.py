import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Property Deal Finder", layout="wide")
st.title("🏘️ Property Deal Finder with BRRR Analysis")

uploaded_file = st.file_uploader("📂 Upload Property CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Simulate yield and rent
    df["Estimated Yield (%)"] = [round(random.uniform(5.0, 6.5), 2) for _ in range(len(df))]
    df["Estimated Rent (£)"] = (df["Price (£)"] * df["Estimated Yield (%)"] / 100) / 12
    df["£/m2"] = df["Price (£)"] / df["Area (m²)"]

    # Deal metrics
    avg_m2 = df["£/m2"].mean()
    df["Undervalued"] = df["£/m2"] < avg_m2 * 0.8
    df["Deal Score"] = ((avg_m2 - df["£/m2"]) / avg_m2 * 100).clip(lower=0).round(1)
    df["Monthly Cash Flow (£)"] = (df["Estimated Rent (£)"] - 350).round(2)
    df["Annual ROI (%)"] = ((df["Monthly Cash Flow (£)"] * 12) / df["Price (£)"] * 100).round(2)

    # BRRR scenario
    df["Refinance Value (£)"] = df["Price (£)"] * 1.2
    df["New Mortgage (£)"] = df["Refinance Value (£)"] * 0.75
    df["Cash Pulled Out (£)"] = (df["New Mortgage (£)"] - df["Price (£)"] * 0.75).clip(lower=0).round(2)

    # Google Maps and badges
    df["Google Maps"] = "https://www.google.com/maps/search/" + df["Address"].str.replace(" ", "+")
    df["Location"] = df["Address"].str.extract(r",\s*([^,]+)$")[0]

    # ✅ New Deal Badge Logic
    def label_deal(row):
        if row["Undervalued"] and row["Annual ROI (%)"] >= 5 and row["Monthly Cash Flow (£)"] > 0:
            return "✅"
        elif row["Annual ROI (%)"] >= 10:
            return "🔥"
        else:
            return "❌"
    df["✅ Deal"] = df.apply(label_deal, axis=1)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Your Deals")
    selected_location = st.sidebar.multiselect("📍 Location", df["Location"].dropna().unique())
    min_roi = st.sidebar.slider("📈 Minimum ROI (%)", 0.0, 20.0, 5.0)
    min_cashflow = st.sidebar.slider("💸 Minimum Monthly Cash Flow (£)", -500, 1000, 0)

    # Filtering logic
    filtered_df = df[
        (df["Undervalued"]) &
        (df["Annual ROI (%)"] >= min_roi) &
        (df["Monthly Cash Flow (£)"] >= min_cashflow)
    ]

    if selected_location:
        filtered_df = filtered_df[filtered_df["Location"].isin(selected_location)]

    st.success(f"✅ {len(filtered_df)} matching undervalued deals found")

    if not filtered_df.empty:
        display_cols = [
            "✅ Deal", "Address", "Price (£)", "Area (m²)", "£/m2",
            "Estimated Rent (£)", "Monthly Cash Flow (£)", "Annual ROI (%)",
            "Cash Pulled Out (£)", "Google Maps"
        ]

        if "Deal Score" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("Deal Score", ascending=False)

        st.dataframe(filtered_df[display_cols])

        st.subheader("📊 ROI vs Property")
        st.bar_chart(filtered_df.set_index("Address")["Annual ROI (%)"])

        st.subheader("💵 Monthly Cash Flow Distribution")
        st.line_chart(filtered_df.set_index("Address")["Monthly Cash Flow (£)"])

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered Deals as CSV",
            data=csv,
            file_name="filtered_property_deals.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No deals matched your filters. Try adjusting ROI or cash flow sliders.")

