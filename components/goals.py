import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def show_goals():
    """
    Display the financial goals tracking page.
    """
    st.title("Financial Goals")
    
    # Create tabs for Set Goals and Track Goals
    tab1, tab2 = st.tabs(["Set Goals", "Track Goals"])
    
    with tab1:
        show_goals_form()
    
    with tab2:
        show_goals_tracking()

def show_goals_form():
    """
    Display the form for setting financial goals.
    """
    st.subheader("Set Financial Goals")
    
    # Create a form for setting goals
    with st.form("goal_form"):
        goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Car, Vacation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_amount = st.number_input("Target Amount ($)", min_value=10.0, step=100.0, value=1000.0)
            current_amount = st.number_input("Current Amount ($)", min_value=0.0, max_value=target_amount, step=100.0, value=0.0)
            
        with col2:
            target_date = st.date_input("Target Date", min_value=datetime.now().date() + timedelta(days=1), value=datetime.now().date() + timedelta(days=365))
            goal_priority = st.select_slider("Priority", options=["Low", "Medium", "High"], value="Medium")
        
        goal_notes = st.text_area("Notes", placeholder="Additional details about this goal...")
        
        # Submit button
        submitted = st.form_submit_button("Add Goal")
        
        if submitted:
            # Create new goal
            new_goal = {
                "name": goal_name,
                "target_amount": str(target_amount),
                "current_amount": str(current_amount),
                "target_date": target_date.strftime("%Y-%m-%d"),
                "priority": goal_priority,
                "notes": goal_notes,
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "progress_updates": []
            }
            
            # Add to session state
            st.session_state.goals.append(new_goal)
            
            st.success(f"Added goal: {goal_name}")
            st.rerun()
    
    # Display existing goals with edit/delete options
    if st.session_state.goals:
        st.markdown("---")
        st.subheader("Edit/Delete Goals")
        
        # Select goal to edit or delete
        goal_names = [goal["name"] for goal in st.session_state.goals]
        selected_goal_name = st.selectbox("Select Goal", goal_names)
        
        # Find the selected goal
        selected_goal_index = goal_names.index(selected_goal_name)
        selected_goal = st.session_state.goals[selected_goal_index]
        
        # Edit form
        with st.form("edit_goal_form"):
            st.markdown(f"### Edit Goal: {selected_goal_name}")
            
            edit_current_amount = st.number_input(
                "Current Amount ($)", 
                min_value=0.0, 
                max_value=float(selected_goal["target_amount"]), 
                value=float(selected_goal["current_amount"]),
                step=50.0
            )
            
            edit_target_date = st.date_input(
                "Target Date", 
                min_value=datetime.now().date(), 
                value=datetime.strptime(selected_goal["target_date"], "%Y-%m-%d").date()
            )
            
            edit_priority = st.select_slider(
                "Priority", 
                options=["Low", "Medium", "High"], 
                value=selected_goal["priority"]
            )
            
            edit_notes = st.text_area("Notes", value=selected_goal["notes"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                update_submitted = st.form_submit_button("Update Goal")
            
            with col2:
                delete_submitted = st.form_submit_button("Delete Goal", type="primary")
        
        if update_submitted:
            # Update goal
            selected_goal["current_amount"] = str(edit_current_amount)
            selected_goal["target_date"] = edit_target_date.strftime("%Y-%m-%d")
            selected_goal["priority"] = edit_priority
            selected_goal["notes"] = edit_notes
            
            # Add progress update if amount changed
            if float(selected_goal["current_amount"]) != edit_current_amount:
                progress_update = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "amount": str(edit_current_amount)
                }
                selected_goal["progress_updates"].append(progress_update)
            
            st.session_state.goals[selected_goal_index] = selected_goal
            st.success(f"Updated goal: {selected_goal_name}")
            st.rerun()
        
        if delete_submitted:
            # Delete goal
            st.session_state.goals.pop(selected_goal_index)
            st.success(f"Deleted goal: {selected_goal_name}")
            st.rerun()

def show_goals_tracking():
    """
    Display goal tracking progress and visualizations.
    """
    if not st.session_state.goals:
        st.info("No goals set yet. Use the 'Set Goals' tab to create your first financial goal.")
        return
    
    st.subheader("Your Financial Goals")
    
    # Summary metrics
    num_goals = len(st.session_state.goals)
    total_target = sum(float(goal["target_amount"]) for goal in st.session_state.goals)
    total_current = sum(float(goal["current_amount"]) for goal in st.session_state.goals)
    overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Goals", num_goals)
    
    with col2:
        st.metric("Total Goal Amount", f"${total_target:.2f}")
    
    with col3:
        st.metric("Overall Progress", f"{overall_progress:.1f}%")
    
    # Progress chart
    goals_data = []
    for goal in st.session_state.goals:
        current = float(goal["current_amount"])
        target = float(goal["target_amount"])
        percent = (current / target * 100) if target > 0 else 0
        
        goals_data.append({
            "name": goal["name"],
            "current": current,
            "target": target,
            "percent": percent,
            "priority": goal["priority"],
            "target_date": goal["target_date"]
        })
    
    if goals_data:
        # Sort by priority
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        goals_data.sort(key=lambda x: priority_order[x["priority"]])
        
        # Create progress chart
        fig = go.Figure()
        
        for goal in goals_data:
            fig.add_trace(go.Bar(
                name=goal["name"],
                y=[goal["name"]],
                x=[goal["percent"]],
                orientation='h',
                text=f"{goal['percent']:.1f}%",
                textposition='auto',
                marker_color=get_priority_color(goal["priority"])
            ))
        
        # Add target line
        for i, goal in enumerate(goals_data):
            fig.add_shape(
                type="line",
                x0=100, x1=100,
                y0=i-0.4, y1=i+0.4,
                line=dict(color="gray", width=2, dash="dash")
            )
        
        fig.update_layout(
            title="Goal Progress",
            xaxis_title="Progress (%)",
            yaxis_title="Goal",
            barmode='group',
            height=max(300, 100 + (len(goals_data) * 50)),
            xaxis=dict(range=[0, 110]),  # Extend a bit past 100% for the target line
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Individual goal details
    st.markdown("---")
    st.subheader("Goal Details")
    
    # Select a goal to view details
    selected_goal_name = st.selectbox(
        "Select a goal to view details",
        [goal["name"] for goal in st.session_state.goals]
    )
    
    # Find the selected goal
    selected_goal = next((goal for goal in st.session_state.goals if goal["name"] == selected_goal_name), None)
    
    if selected_goal:
        # Calculate progress
        current_amount = float(selected_goal["current_amount"])
        target_amount = float(selected_goal["target_amount"])
        progress_percent = (current_amount / target_amount * 100) if target_amount > 0 else 0
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Amount", f"${current_amount:.2f}")
        
        with col2:
            st.metric("Target Amount", f"${target_amount:.2f}")
        
        with col3:
            st.metric("Progress", f"{progress_percent:.1f}%")
        
        # Progress bar
        st.progress(min(progress_percent / 100, 1.0))
        
        # Timeline info
        target_date = datetime.strptime(selected_goal["target_date"], "%Y-%m-%d").date()
        days_remaining = (target_date - datetime.now().date()).days
        
        if days_remaining > 0:
            # Calculate required savings per month to reach goal
            remaining_amount = target_amount - current_amount
            months_remaining = max(days_remaining / 30, 0.1)  # Avoid division by zero
            monthly_savings_needed = remaining_amount / months_remaining
            
            st.markdown(f"**Time remaining:** {days_remaining} days ({int(months_remaining)} months)")
            st.markdown(f"**Required monthly savings:** ${monthly_savings_needed:.2f}")
            
            # Check if on track
            on_track = current_amount >= (target_amount * (1 - (days_remaining / 365)))
            
            if on_track:
                st.success("You're on track to reach your goal on time!")
            else:
                st.warning("You may need to increase your savings rate to reach this goal on time.")
        else:
            if progress_percent >= 100:
                st.success("Goal achieved! 🎉")
            else:
                st.error("Goal deadline has passed. Consider updating your target date.")
        
        # Display notes
        if selected_goal.get("notes"):
            st.markdown("**Notes:**")
            st.markdown(selected_goal["notes"])
        
        # Display progress history
        if selected_goal.get("progress_updates"):
            st.markdown("---")
            st.subheader("Progress History")
            
            # Convert to dataframe
            updates = selected_goal["progress_updates"]
            if updates:
                # Add created date as first update
                updates = [{
                    "date": selected_goal["created_date"],
                    "amount": "0" if not updates else updates[0]["amount"]
                }] + updates
                
                # Create dataframe
                updates_df = pd.DataFrame(updates)
                updates_df["date"] = pd.to_datetime(updates_df["date"])
                updates_df["amount"] = updates_df["amount"].astype(float)
                updates_df = updates_df.sort_values("date")
                
                # Create line chart
                fig = px.line(
                    updates_df,
                    x="date",
                    y="amount",
                    title="Progress Over Time",
                    markers=True
                )
                
                # Add target line
                fig.add_hline(
                    y=target_amount,
                    line_dash="dash",
                    line_color="green",
                    annotation_text="Target"
                )
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Amount ($)",
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No progress updates recorded yet.")
        
        # Goal strategies
        st.markdown("---")
        st.subheader("Goal Strategies")
        
        # Generate simple strategies based on goal type and amount
        goal_name_lower = selected_goal_name.lower()
        
        if "emergency" in goal_name_lower or "fund" in goal_name_lower:
            st.markdown("""
            ### Emergency Fund Tips:
            - Aim to save 3-6 months of essential expenses
            - Set up automatic transfers to a high-yield savings account
            - Use windfalls (tax refunds, bonuses) to boost your emergency fund
            - Keep this money in a liquid account that's easily accessible
            """)
        elif "car" in goal_name_lower or "vehicle" in goal_name_lower:
            st.markdown("""
            ### Vehicle Savings Tips:
            - Research average costs for your desired vehicle type
            - Consider certified pre-owned vehicles to save money
            - Save for a larger down payment to reduce financing costs
            - Don't forget to budget for taxes, registration, and insurance
            """)
        elif "house" in goal_name_lower or "home" in goal_name_lower:
            st.markdown("""
            ### Home Savings Tips:
            - Aim for a 20% down payment to avoid PMI
            - Look into first-time homebuyer programs
            - Save for closing costs (typically 2-5% of loan amount)
            - Build your credit score to qualify for better rates
            """)
        elif "vacation" in goal_name_lower or "travel" in goal_name_lower:
            st.markdown("""
            ### Travel Savings Tips:
            - Set up a dedicated travel fund
            - Look for travel deals during off-peak seasons
            - Consider using travel rewards credit cards
            - Set price alerts for flights to your desired destination
            """)
        elif "education" in goal_name_lower or "college" in goal_name_lower:
            st.markdown("""
            ### Education Savings Tips:
            - Consider tax-advantaged education accounts like 529 plans
            - Look into scholarships and grants
            - Start saving early to take advantage of compound interest
            - Research schools with the best value for your desired program
            """)
        elif "wedding" in goal_name_lower:
            st.markdown("""
            ### Wedding Savings Tips:
            - Create a detailed wedding budget
            - Consider off-season or weekday weddings for discounts
            - Look for areas where you can DIY to save money
            - Prioritize what's most important and allocate funds accordingly
            """)
        else:
            st.markdown("""
            ### General Savings Tips:
            - Break your goal into smaller milestones
            - Set up automatic transfers to your savings account
            - Reduce unnecessary expenses to increase your savings rate
            - Track your progress regularly and adjust your strategy as needed
            """)

def get_priority_color(priority):
    """
    Return color for priority level.
    """
    if priority == "High":
        return "#EF5350"  # Red
    elif priority == "Medium":
        return "#FFA726"  # Orange
    else:
        return "#66BB6A"  # Green
