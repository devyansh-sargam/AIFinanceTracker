"""Utility functions for UI enhancements and animations."""

import streamlit as st
import os
import base64
from pathlib import Path
from static.icons import (
    dashboard_icon, expenses_icon, budget_icon, goals_icon, insights_icon,
    money_icon, profile_icon, logout_icon, calendar_icon, savings_icon,
    analysis_icon, alert_icon, success_icon, info_icon, warning_icon,
    finance_illustration, goals_illustration, savings_illustration,
    expenses_illustration, profile_illustration
)

def load_css():
    """Load custom CSS."""
    css_path = Path("static/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning("CSS file not found.")

def add_animation_css():
    """Add basic animation CSS if the full CSS file is not available."""
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        0% { transform: translateX(-50px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        0% { transform: translateX(50px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0, 230, 118, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 230, 118, 0.8); }
        100% { box-shadow: 0 0 5px rgba(0, 230, 118, 0.5); }
    }
    
    .animated-card {
        animation: fadeIn 0.8s ease-in-out, glow 3s infinite;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(30, 30, 30, 0.7);
        border: 1px solid rgba(0, 230, 118, 0.3);
        margin-bottom: 20px;
    }
    
    .animated-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
    }
    
    .animated-page {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .finance-image {
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 1s ease-in-out;
    }
    
    .finance-image:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def add_logo():
    """Add the finance assistant logo."""
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 1s ease-in-out;">
        <h1 style="color: #00E676; margin-bottom: 0;">
            <span style="animation: glow 2s infinite;">💰</span> 
            Finance Assistant
        </h1>
        <p style="color: #AAAAAA; margin-top: 0;">Your AI-powered personal finance manager</p>
    </div>
    """, unsafe_allow_html=True)

def animated_text(text, animation="fadeIn", color="#FFFFFF", font_size="1rem", margin="0", tag="p"):
    """Display animated text."""
    st.markdown(f"""
    <{tag} style="color: {color}; font-size: {font_size}; margin: {margin}; animation: {animation} 1s ease-in-out;">
        {text}
    </{tag}>
    """, unsafe_allow_html=True)

def animated_metric(label, value, prefix="", suffix="", color="#00E676", animation="slideInRight"):
    """Display an animated metric value."""
    st.markdown(f"""
    <div style="animation: fadeIn 0.8s ease-in-out;">
        <p style="color: #AAAAAA; margin-bottom: 5px; font-size: 1rem; animation: {animation} 0.7s ease-in-out;">
            {label}
        </p>
        <h2 style="color: {color}; margin-top: 0; font-size: 2.5rem; animation: {animation} 0.5s ease-in-out;">
            {prefix}{value}{suffix}
        </h2>
    </div>
    """, unsafe_allow_html=True)

def animated_card(content, animation="fadeIn", glow=True):
    """Display content in an animated card."""
    glow_class = "glow" if glow else ""
    st.markdown(f"""
    <div class="animated-card {glow_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)

def animated_divider():
    """Display an animated divider."""
    st.markdown("""
    <div style="margin: 20px 0; height: 2px; background: linear-gradient(90deg, 
                rgba(0,230,118,0), rgba(0,230,118,0.8), rgba(0,230,118,0)); 
                animation: fadeIn 1s ease-in-out;"></div>
    """, unsafe_allow_html=True)

def animated_progress_bar(value, max_value=100, label=None):
    """Display an animated progress bar."""
    percentage = min(100, int((value / max_value) * 100))
    label_text = f"{label}: " if label else ""
    
    st.markdown(f"""
    <div style="margin: 10px 0;">
        <p style="color: #AAAAAA; margin-bottom: 5px; animation: fadeIn 0.5s ease-in-out;">
            {label_text}{percentage}%
        </p>
        <div class="animated-progress">
            <div class="animated-progress-bar" style="width: {percentage}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_icon(icon, tooltip=None):
    """Display an SVG icon with optional tooltip."""
    if tooltip:
        st.markdown(f"""
        <div class="custom-tooltip">
            {icon}
            <span class="tooltip-text">{tooltip}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(icon, unsafe_allow_html=True)

def page_header(title, icon=None, description=None):
    """Display a page header with icon and description."""
    icon_html = icon if icon else ""
    desc_html = f'<p style="color: #AAAAAA; margin-top: 5px; animation: fadeIn 1.2s ease-in-out;">{description}</p>' if description else ""
    
    st.markdown(f"""
    <div style="animation: fadeIn 0.8s ease-in-out; margin-bottom: 20px;">
        <h2 style="color: #00E676; display: flex; align-items: center; animation: slideInRight 0.5s ease-in-out;">
            {icon_html} {title}
        </h2>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)

def animated_illustration(illustration):
    """Display an animated SVG illustration."""
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0; animation: fadeIn 1s ease-in-out;">
        {illustration}
    </div>
    """, unsafe_allow_html=True)

def notification(message, type="info"):
    """Display a styled notification."""
    icon_map = {
        "success": success_icon,
        "info": info_icon,
        "warning": warning_icon,
        "error": alert_icon
    }
    
    color_map = {
        "success": "#00E676",
        "info": "#2196F3",
        "warning": "#FFC107",
        "error": "#FF5252"
    }
    
    icon = icon_map.get(type, info_icon)
    color = color_map.get(type, "#2196F3")
    
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; 
              background-color: rgba({color.replace('#', '')}, 0.1); 
              border: 1px solid {color};
              display: flex; align-items: center;
              animation: fadeIn 0.5s ease-in-out;">
        {icon}
        <span style="margin-left: 10px; color: #FFFFFF;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def display_dashboard_widgets():
    """Display animated widgets for dashboard."""
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0;">
        <div class="metric-card">
            <div class="metric-value">$2,850</div>
            <div class="metric-label">Monthly Income</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">$1,720</div>
            <div class="metric-label">Monthly Expenses</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">$1,130</div>
            <div class="metric-label">Monthly Savings</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">42%</div>
            <div class="metric-label">Saving Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def animated_button(label, key=None, type="primary", icon=None, help=None):
    """Create a styled and animated button."""
    # Need to return the button result
    button_key = key if key else f"button_{label.lower().replace(' ', '_')}"
    icon_html = icon if icon else ""
    
    if type == "primary":
        button_style = "background-color: #00E676; color: #121212;"
    else:
        button_style = "background-color: rgba(255, 255, 255, 0.1); color: #FFFFFF; border: 1px solid rgba(255, 255, 255, 0.2);"
    
    # Unfortunately, we can't directly style Streamlit buttons with CSS
    # So we'll use a regular Streamlit button but add animation class
    st.markdown(f"""
    <style>
    div[data-testid="stButton"] button[kind="{type}"] {{
        width: 100%;
        {button_style}
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }}
    div[data-testid="stButton"] button[kind="{type}"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 230, 118, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    help_text = help if help else f"Click to {label.lower()}"
    return st.button(f"{icon_html} {label}", key=button_key, help=help_text, type=type, use_container_width=True)

def hover_effect(element_id):
    """Add hover effect to an element by ID."""
    st.markdown(f"""
    <style>
    #{element_id}:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    </style>
    """, unsafe_allow_html=True)

def smooth_scroll():
    """Add smooth scrolling to the page and detect scrolling for scrollbar effects."""
    st.markdown("""
    <style>
    html {
        scroll-behavior: smooth;
    }
    </style>
    
    <script>
    // Add scroll detection for improved scrollbar effects
    document.addEventListener('DOMContentLoaded', function() {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                document.body.classList.add('scrolled');
            } else {
                document.body.classList.remove('scrolled');
            }
        });
        
        // Add hover effects to interactive elements
        document.querySelectorAll('.stButton button').forEach(function(button) {
            button.addEventListener('mouseover', function() {
                this.style.transform = 'translateY(-3px)';
                this.style.boxShadow = '0 10px 20px rgba(0, 230, 118, 0.3)';
            });
            
            button.addEventListener('mouseout', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 5px 10px rgba(0, 230, 118, 0.1)';
            });
            
            button.addEventListener('mousedown', function() {
                this.style.transform = 'translateY(-1px)';
            });
            
            button.addEventListener('mouseup', function() {
                this.style.transform = 'translateY(-3px)';
            });
        });
        
        // Add hover effects to chart elements
        document.querySelectorAll('.js-plotly-plot').forEach(function(chart) {
            chart.addEventListener('mouseover', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.2), 0 0 30px rgba(0, 230, 118, 0.2)';
            });
            
            chart.addEventListener('mouseout', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
            });
        });
        
        // Add shine effect to cards on hover
        document.querySelectorAll('.metric-card, .animated-card').forEach(function(card) {
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                this.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(0, 230, 118, 0.1), transparent 50%), rgba(30, 30, 30, 0.7)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.background = 'rgba(30, 30, 30, 0.7)';
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def get_local_image(image_path):
    """Get base64 encoded image for local display."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return None

def display_footer():
    """Display an animated footer."""
    st.markdown("""
    <div class="custom-footer">
        <p style="color: #AAAAAA;">© 2025 Finance Assistant | AI-Powered Personal Finance Management</p>
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <a href="#" style="color: #00E676; text-decoration: none; margin: 0 10px;">About</a>
            <a href="#" style="color: #00E676; text-decoration: none; margin: 0 10px;">Privacy</a>
            <a href="#" style="color: #00E676; text-decoration: none; margin: 0 10px;">Terms</a>
            <a href="#" style="color: #00E676; text-decoration: none; margin: 0 10px;">Support</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_illustration(name):
    """Get an illustration by name."""
    illustrations = {
        "finance": finance_illustration,
        "goals": goals_illustration,
        "savings": savings_illustration,
        "expenses": expenses_illustration,
        "profile": profile_illustration,
    }
    return illustrations.get(name, finance_illustration)

def get_icon(name):
    """Get an icon by name."""
    icons = {
        "dashboard": dashboard_icon,
        "expenses": expenses_icon,
        "budget": budget_icon,
        "goals": goals_icon,
        "insights": insights_icon,
        "money": money_icon,
        "profile": profile_icon,
        "logout": logout_icon,
        "calendar": calendar_icon,
        "savings": savings_icon,
        "analysis": analysis_icon,
        "alert": alert_icon,
        "success": success_icon,
        "info": info_icon,
        "warning": warning_icon,
    }
    return icons.get(name, info_icon)