import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Quantum Task Explorer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for quantum theme
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background: #1a1625;
    }
    .stButton>button {
        background: linear-gradient(to right, #ff00cc, #3333ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
    }
    .task-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #00ffff;
    }
    .quantum-meter {
        background: #3333ff;
        height: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=['Task', 'Priority', 'Quantum State', 'Created', 'Completed'])

# Sidebar
with st.sidebar:
    st.title("⚛️ Quantum Control Panel")
    
    # Task input
    new_task = st.text_input("Enter New Task")
    priority = st.slider("Priority (1-5)", 1, 5, 3)
    
    if st.button("Entangle Task"):
        if new_task:
            new_task_data = {
                'Task': new_task,
                'Priority': priority,
                'Quantum State': random.choice(['Superposition', 'Entangled', 'Collapsed']),
                'Created': datetime.now(),
                'Completed': False
            }
            st.session_state.tasks = pd.concat(
                [st.session_state.tasks, pd.DataFrame([new_task_data])],
                ignore_index=True
            )
            st.success("Task quantum-encoded successfully!")

    # Quantum controls
    st.subheader("Quantum Operations")
    if st.button("Randomize States"):
        st.session_state.tasks['Quantum State'] = [random.choice(['Superposition', 'Entangled', 'Collapsed']) 
                                                 for _ in range(len(st.session_state.tasks))]
        st.rerun()

# Main content
st.title("Quantum Task Explorer")
st.write("Manage your tasks in a quantum-dimensional space!")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Task Grid", "Quantum Visualization", "Analytics"])

with tab1:
    st.subheader("Task Grid")
    if not st.session_state.tasks.empty:
        for idx, row in st.session_state.tasks.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                        <div class='task-card'>
                            <strong>{row['Task']}</strong><br>
                            State: {row['Quantum State']}<br>
                            Created: {row['Created'].strftime('%Y-%m-%d %H:%M')}
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write(f"Priority: {row['Priority']}")
                    st.progress(row['Priority'] / 5)
                with col3:
                    if st.button("Complete", key=f"complete_{idx}"):
                        st.session_state.tasks.loc[idx, 'Completed'] = True
                        st.session_state.tasks.loc[idx, 'Quantum State'] = 'Collapsed'
                        st.rerun()
    else:
        st.info("No tasks in quantum space yet. Add some tasks!")

with tab2:
    st.subheader("Quantum Visualization")
    if not st.session_state.tasks.empty:
        # Convert Priority to numeric type and ensure compatibility
        tasks_df = st.session_state.tasks.copy()
        tasks_df['Priority'] = pd.to_numeric(tasks_df['Priority'], errors='coerce')
        
        # 3D Scatter plot of tasks
        fig = px.scatter_3d(
            tasks_df,
            x='Priority',
            y=tasks_df.index,
            z='Created',
            color='Quantum State',
            size=tasks_df['Priority'].to_numpy(),  # Convert to NumPy array
            hover_data=['Task'],
            color_discrete_map={
                'Superposition': '#ff00cc',
                'Entangled': '#00ffff',
                'Collapsed': '#33ff33'
            },
            title="Quantum Task Space"
        )
        fig.update_layout(
            scene=dict(
                xaxis_title="Priority",
                yaxis_title="Task ID",
                zaxis_title="Time",
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Quantum space empty - visualize tasks by adding some!")

with tab3:
    st.subheader("Quantum Analytics")
    if not st.session_state.tasks.empty:
        # Task distribution
        state_counts = st.session_state.tasks['Quantum State'].value_counts()
        st.bar_chart(state_counts)
        
        # Priority distribution
        priority_counts = st.session_state.tasks['Priority'].value_counts()
        st.area_chart(priority_counts)
        
        # Completion stats
        completed = len(st.session_state.tasks[st.session_state.tasks['Completed']])
        total = len(st.session_state.tasks)
        st.metric("Completion Rate", f"{(completed/total)*100:.1f}%", f"{completed}/{total}")
    else:
        st.write("No analytics available - add tasks to analyze!")

# Quantum animation
st.markdown("---")
st.write("Quantum Processing Status")
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
    if i == 99:
        progress_bar.empty()
        st.write("Quantum systems nominal")
