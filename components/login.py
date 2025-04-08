import streamlit as st
from utils.auth import show_login_ui, show_signup_ui, demo_login
from utils.ui_utils import (
    add_logo, animated_text, animated_card, animated_divider, 
    animated_illustration, notification, display_footer,
    get_illustration, get_icon
)

def show_login_page():
    """
    Display the login page with enhanced UI and animations.
    """
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Animated logo and title
        st.markdown(
            """
            <div style="text-align: center; animation: fadeIn 1.5s ease-in-out;">
                <h1 style="color: #00E676; text-shadow: 0 0 15px rgba(0, 230, 118, 0.8); 
                         margin-bottom: 0.5rem; font-size: 2.5rem;">
                    <span style="display: inline-block; animation: pulse 2s infinite;">💰</span> 
                    Finance Assistant
                </h1>
                <p style="color: rgba(255,255,255,0.8); font-style: italic; 
                        margin-top: 0; margin-bottom: 20px; font-size: 1.2rem;">
                    Your AI-powered financial advisor
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display a finance illustration
        animated_illustration(get_illustration("finance"))
        
        # Features highlight cards with animations
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                 gap: 15px; margin: 20px 0;">
            <div class="animated-card" style="text-align: center; padding: 15px;">
                <div style="font-size: 2rem; color: #00E676; margin-bottom: 10px;">📊</div>
                <h4 style="color: #00E676; margin: 0;">Track Expenses</h4>
                <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">
                    Monitor all your spending in one place
                </p>
            </div>
            <div class="animated-card" style="text-align: center; padding: 15px;">
                <div style="font-size: 2rem; color: #00E676; margin-bottom: 10px;">💼</div>
                <h4 style="color: #00E676; margin: 0;">Manage Budgets</h4>
                <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">
                    Create and stick to your financial plan
                </p>
            </div>
            <div class="animated-card" style="text-align: center; padding: 15px;">
                <div style="font-size: 2rem; color: #00E676; margin-bottom: 10px;">🎯</div>
                <h4 style="color: #00E676; margin: 0;">Set Goals</h4>
                <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">
                    Achieve your financial dreams
                </p>
            </div>
            <div class="animated-card" style="text-align: center; padding: 15px;">
                <div style="font-size: 2rem; color: #00E676; margin-bottom: 10px;">🧠</div>
                <h4 style="color: #00E676; margin: 0;">AI Insights</h4>
                <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">
                    Get smart recommendations
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        animated_divider()
        
        # Create tabs for login and signup with custom styling
        st.markdown("""
        <style>
        div[data-testid="stTabs"] > div[data-testid="stTabsHeader"] {
            background-color: rgba(30, 30, 30, 0.3);
            border-radius: 10px 10px 0 0;
            padding: 5px 5px 0 5px;
        }
        div[data-testid="stTabs"] > div[data-testid="stTabsHeader"] button {
            border-radius: 10px 10px 0 0;
            padding: 10px 16px;
            background-color: rgba(30, 30, 30, 0.7);
            border: none;
            color: #AAAAAA;
            transition: all 0.3s ease;
        }
        div[data-testid="stTabs"] > div[data-testid="stTabsHeader"] button:hover {
            background-color: rgba(0, 230, 118, 0.1);
            color: #00E676;
        }
        div[data-testid="stTabs"] > div[data-testid="stTabsHeader"] button[aria-selected="true"] {
            background-color: rgba(0, 230, 118, 0.2);
            color: #00E676;
            border-bottom: 2px solid #00E676;
            font-weight: bold;
        }
        div[data-testid="stTabs"] > div[data-testid="stTabContent"] {
            background-color: rgba(30, 30, 30, 0.3);
            border-radius: 0 0 10px 10px;
            padding: 20px;
            animation: fadeIn 0.5s ease-in-out;
        }
        </style>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Demo Mode"])
        
        with tab1:
            st.markdown("""
            <div style="animation: fadeIn 0.8s ease-in-out; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #00E676;">Welcome Back</h3>
                <p style="color: #AAAAAA;">Log in to access your financial dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            show_login_ui()
        
        with tab2:
            st.markdown("""
            <div style="animation: fadeIn 0.8s ease-in-out; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #00E676;">Join Finance Assistant</h3>
                <p style="color: #AAAAAA;">Create an account to start your financial journey</p>
            </div>
            """, unsafe_allow_html=True)
            show_signup_ui()
            
        with tab3:
            st.markdown("""
            <div style="animation: fadeIn 0.8s ease-in-out; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #FFD700;">Try Demo Mode</h3>
                <p style="color: #AAAAAA;">Explore the app with sample data</p>
            </div>
            """, unsafe_allow_html=True)
            demo_login()
        
        # Testimonials with animations
        animated_divider()
        
        st.markdown("""
        <div style="margin-top: 30px; animation: fadeIn 1s ease-in-out;">
            <h3 style="color: #00E676; text-align: center; margin-bottom: 20px;">
                What Our Users Say
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div class="animated-card" style="padding: 20px;">
                    <p style="color: #AAAAAA; font-style: italic;">
                        "Finance Assistant helped me save an extra $300 per month by identifying unnecessary subscriptions 
                        and recommending budget adjustments."
                    </p>
                    <p style="color: #00E676; margin-bottom: 0;">Sarah T.</p>
                    <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">Marketing Manager</p>
                </div>
                
                <div class="animated-card" style="padding: 20px;">
                    <p style="color: #AAAAAA; font-style: italic;">
                        "The AI insights are incredibly helpful. It's like having a financial advisor available 24/7 
                        that knows all my spending habits."
                    </p>
                    <p style="color: #00E676; margin-bottom: 0;">Michael K.</p>
                    <p style="color: #AAAAAA; margin-top: 5px; font-size: 0.9rem;">Software Developer</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer with animated entrance
        st.markdown(
            """
            <div style="margin-top: 40px; text-align: center; animation: slideInUp 0.8s ease-in-out;">
                <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                    <a href="#" style="color: #00E676; text-decoration: none; margin: 0 15px;">About</a>
                    <a href="#" style="color: #00E676; text-decoration: none; margin: 0 15px;">Features</a>
                    <a href="#" style="color: #00E676; text-decoration: none; margin: 0 15px;">Pricing</a>
                    <a href="#" style="color: #00E676; text-decoration: none; margin: 0 15px;">Contact</a>
                </div>
                <p style="margin: 10px 0; color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                    © 2025 Finance Assistant. All rights reserved.
                </p>
                <p style="margin: 5px 0; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
                    Powered by AI for better financial decisions
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )