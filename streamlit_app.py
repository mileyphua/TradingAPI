import streamlit as st
import requests
import json
import sqlite3
from datetime import datetime
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Trading Webhook Proxy",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #4285f4 0%, #34a853 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.webhook-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    background: #171717;
}
.trading-button {
    width: 100%;
    margin: 0.5rem 0;
}
.success-message {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
}
.error-message {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# Database functions
@st.cache_resource
def init_db():
    conn = sqlite3.connect('webhooks.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS webhooks
                 (id INTEGER PRIMARY KEY, name TEXT, url TEXT, active BOOLEAN)''')
    conn.commit()
    return conn

def add_webhook(name, url):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO webhooks (name, url, active) VALUES (?, ?, ?)", 
              (name, url, True))
    conn.commit()

@st.cache_data(ttl=60)
def get_webhooks():
    conn = init_db()
    df = pd.read_sql_query("SELECT * FROM webhooks WHERE active = 1", conn)
    return df

def delete_webhook(webhook_id):
    conn = init_db()
    c = conn.cursor()
    c.execute("UPDATE webhooks SET active = 0 WHERE id = ?", (webhook_id,))
    conn.commit()

def send_trading_signal(webhook_url, instrument, action):
    """Send trading signal with exact JSON format as requested"""
    body_string = f"description : JMA US500 v3 (10,000, 0.1, 100, Fixed, , 2, 50, 0, 10, close, 33, 63, 9, 10, Default, 2, Solid, 1.5, 1W, 85, 2.4, 0.3, 2, 0.8, 0, 14, 20, 5, top_right, bottom_left, 1, 1, 20, 5)\ntimestamp : 30\nticker : {instrument}\naction: {action} \ncontracts: 100 \nposition_size: {'0' if action == 'exit' else '100'}\ncomment : {'Buy' if action == 'buy' else 'Sell' if action == 'sell' else 'Exit Long'}"
    
    # Exact JSON format as requested by user
    payload = body_string
    
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200, response.status_code
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

# Initialize database
init_db()

# Main header
st.markdown("""
<div class="main-header">
    <h1>📈 Trading Webhook Proxy</h1>
    <p>Forward Trading alerts to your Cloud Server seamlessly</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for webhook management
st.sidebar.header("🔧 Webhook Management")

with st.sidebar.expander("Add New Webhook", expanded=False):
    with st.form("add_webhook"):
        webhook_name = st.text_input("Webhook Name", placeholder="e.g., BTC Trading Alerts")
        webhook_url = st.text_input("Webhook URL", placeholder="https://your-webhook-url.com")
        
        if st.form_submit_button("Add Webhook"):
            if webhook_name and webhook_url:
                add_webhook(webhook_name, webhook_url)
                st.success(f"Added webhook: {webhook_name}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Please fill in all fields")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Trading Actions")
    
    # Get webhooks
    webhooks_df = get_webhooks()
    
    if len(webhooks_df) > 0:
        # Webhook selection
        webhook_options = ["All Webhooks"] + webhooks_df['name'].tolist()
        selected_webhook = st.selectbox("Select Webhook Configuration", webhook_options)
        
        # Instrument selection
        instrument = st.selectbox("Trading Instrument", 
                                ["GOLD", "US100", "US30", "US500", "DE40"])
        
        # Trading buttons
        col_buy, col_sell, col_exit = st.columns(3)
        
        with col_buy:
            if st.button("🟢 BUY", key="buy_btn", help="Send BUY signal", use_container_width=True):
                if selected_webhook == "All Webhooks":
                    success_count = 0
                    total_count = len(webhooks_df)
                    results = []
                    
                    for _, webhook in webhooks_df.iterrows():
                        success, status = send_trading_signal(webhook['url'], instrument, 'buy')
                        if success:
                            success_count += 1
                        results.append(f"• {webhook['name']}: {'✅ Success' if success else f'❌ Failed ({status})'}")
                    
                    if success_count > 0:
                        st.success(f"BUY signal sent to {success_count}/{total_count} webhooks successfully!")
                    else:
                        st.error(f"Failed to send BUY signal to all {total_count} webhooks")
                    
                    with st.expander("View Details"):
                        for result in results:
                            st.write(result)
                else:
                    webhook_url = webhooks_df[webhooks_df['name'] == selected_webhook]['url'].iloc[0]
                    success, status = send_trading_signal(webhook_url, instrument, 'buy')
                    if success:
                        st.success("BUY signal sent successfully!")
                    else:
                        st.error(f"Failed to send BUY signal: {status}")
        
        with col_sell:
            if st.button("🟡 SELL", key="sell_btn", help="Send SELL signal", use_container_width=True):
                if selected_webhook == "All Webhooks":
                    success_count = 0
                    total_count = len(webhooks_df)
                    results = []
                    
                    for _, webhook in webhooks_df.iterrows():
                        success, status = send_trading_signal(webhook['url'], instrument, 'sell')
                        if success:
                            success_count += 1
                        results.append(f"• {webhook['name']}: {'✅ Success' if success else f'❌ Failed ({status})'}")
                    
                    if success_count > 0:
                        st.success(f"SELL signal sent to {success_count}/{total_count} webhooks successfully!")
                    else:
                        st.error(f"Failed to send SELL signal to all {total_count} webhooks")
                    
                    with st.expander("View Details"):
                        for result in results:
                            st.write(result)
                else:
                    webhook_url = webhooks_df[webhooks_df['name'] == selected_webhook]['url'].iloc[0]
                    success, status = send_trading_signal(webhook_url, instrument, 'sell')
                    if success:
                        st.success("SELL signal sent successfully!")
                    else:
                        st.error(f"Failed to send SELL signal: {status}")
        
        with col_exit:
            if st.button("🔴 EXIT", key="exit_btn", help="Send EXIT signal", use_container_width=True):
                if selected_webhook == "All Webhooks":
                    success_count = 0
                    total_count = len(webhooks_df)
                    results = []
                    
                    for _, webhook in webhooks_df.iterrows():
                        success, status = send_trading_signal(webhook['url'], instrument, 'exit')
                        if success:
                            success_count += 1
                        results.append(f"• {webhook['name']}: {'✅ Success' if success else f'❌ Failed ({status})'}")
                    
                    if success_count > 0:
                        st.success(f"EXIT signal sent to {success_count}/{total_count} webhooks successfully!")
                    else:
                        st.error(f"Failed to send EXIT signal to all {total_count} webhooks")
                    
                    with st.expander("View Details"):
                        for result in results:
                            st.write(result)
                else:
                    webhook_url = webhooks_df[webhooks_df['name'] == selected_webhook]['url'].iloc[0]
                    success, status = send_trading_signal(webhook_url, instrument, 'exit')
                    if success:
                        st.success("EXIT signal sent successfully!")
                    else:
                        st.error(f"Failed to send EXIT signal: {status}")
        
        # JSON Format Display
        st.subheader("📋 JSON Payload Format")
        with st.expander("View Current JSON Format", expanded=False):
            sample_payload = "description : JMA US500 v3 (10,000, 0.1, 100, Fixed, , 2, 50, 0, 10, close, 33, 63, 9, 10, Default, 2, Solid, 1.5, 1W, 85, 2.4, 0.3, 2, 0.8, 0, 14, 20, 5, top_right, bottom_left, 1, 1, 20, 5)\\ntimestamp : 30\\nticker : {instrument}\\naction: sell \\ncontracts: 100 \\nposition_size: 0\\ncomment : Exit Long"
            
            st.json(sample_payload)
    else:
        st.warning("No webhooks configured. Please add a webhook in the sidebar.")

with col2:
    st.header("📋 Active Webhooks")
    
    if len(webhooks_df) > 0:
        for _, webhook in webhooks_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="webhook-card">
                    <h4>{webhook['name']}</h4>
                    <p><small>🔗 {webhook['url'][50:]}...</small></p>
                    <span style="color: green;">● Active</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"delete_{webhook['id']}", help=f"Delete {webhook['name']}"):
                    delete_webhook(webhook['id'])
                    st.cache_data.clear()
                    st.rerun()
    else:
        st.info("No active webhooks")

# Instructions section
st.markdown("---")
st.header("📖 How to Use")

col_inst1, col_inst2, col_inst3 = st.columns(3)

with col_inst1:
    st.markdown("""
    ### 1️⃣ Add Webhook
    - Use the sidebar to add your webhook URL
    - Give it a descriptive name
    - Click "Add Webhook"
    """)

with col_inst2:
    st.markdown("""
    ### 2️⃣ Select Configuration
    - Choose a specific webhook or "All Webhooks"
    - Select your trading instrument
    - Choose your action (BUY/SELL/EXIT)
    """)

with col_inst3:
    st.markdown("""
    ### 3️⃣ Send Signals
    - Click the trading button
    - View real-time status
    - Check results and details
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Trading Webhook Proxy v2.0</strong> | Built with Streamlit</p>
    <p>🔒 Secure • 🚀 Fast • 📱 Responsive</p>
</div>
""", unsafe_allow_html=True)

