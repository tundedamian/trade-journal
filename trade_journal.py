# NOTE: To run this dashboard, ensure you have Streamlit installed.
# You can install it using: pip install streamlit

import streamlit as st
import pandas as pd
import datetime

# --- Page Config ---
st.set_page_config(page_title="Trade Journal & PnL Tracker", layout="wide")
st.title("📈 Trade Journal & PnL Tracker")

# --- Initialize Session State for Trade Records ---
if "trades" not in st.session_state:
    st.session_state.trades = []

# --- Trade Entry Form ---
st.sidebar.header("New Trade Entry")
with st.sidebar.form("trade_form"):
    date = st.date_input("Trade Date", value=datetime.date.today())
    asset = st.text_input("Asset (e.g., BTCUSDT)")
    strategy = st.selectbox("Strategy Type", ["Momentum", "Mean Reversion", "Narrative", "Arbitrage", "Other"])
    entry_price = st.number_input("Entry Price", min_value=0.0, format="%.4f")
    exit_price = st.number_input("Exit Price", min_value=0.0, format="%.4f")
    capital = st.number_input("Capital Used ($)", min_value=0.0, format="%.2f")
    notes = st.text_area("Trade Notes")
    submitted = st.form_submit_button("Add Trade")

    if submitted:
        pnl = (exit_price - entry_price) * (capital / entry_price) if entry_price else 0.0
        st.session_state.trades.append({
            "Date": date,
            "Asset": asset.upper(),
            "Strategy": strategy,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Capital ($)": capital,
            "PnL ($)": round(pnl, 2),
            "Result": "Win" if pnl > 0 else ("Loss" if pnl < 0 else "Break-even"),
            "Notes": notes
        })
        st.success("Trade added successfully!")

# --- Display Trade Table ---
if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)

    st.subheader("📋 Trade History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

    # --- Summary Statistics ---
    st.subheader("📊 Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades", len(df))
    with col2:
        st.metric("Total PnL ($)", round(df["PnL ($)"].sum(), 2))
    with col3:
        st.metric("Win Rate", f"{(df['Result'].value_counts().get('Win', 0) / len(df)) * 100:.2f}%")
    with col4:
        st.metric("Avg PnL per Trade", round(df["PnL ($)"].mean(), 2))

    # --- PnL by Strategy ---
    st.subheader("🧠 PnL by Strategy")
    pnl_by_strategy = df.groupby("Strategy")["PnL ($)"].sum().sort_values(ascending=False)
    st.bar_chart(pnl_by_strategy)

    # --- Export Option ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📅 Download Trade History as CSV",
        data=csv,
        file_name='trade_journal.csv',
        mime='text/csv',
    )
else:
    st.info("No trades logged yet. Use the form on the left to add one.")
