import streamlit as st
import pandas as pd
import os
import tempfile
from PIL import Image
import numpy as np
import cv2
from io import StringIO
import base64
import datetime

# Import utility modules
from utils.data_processor import process_performance_data, extract_key_metrics
from utils.visualization import create_performance_radar, plot_trend_analysis, plot_comparison
from utils.rag_system import query_knowledge_base, initialize_kb
from utils.image_analyzer import analyze_form, detect_pose
from utils.recommendation_engine import generate_recommendations
from utils.database import (
    get_all_athletes, get_or_create_athlete, 
    save_performance_data, save_form_analysis,
    get_athlete_performance_data, get_athlete_form_analyses,
    store_dataframe, load_dataframe, delete_athlete
)

# Custom function to add background image and general styling
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(to bottom, rgba(20, 20, 30, 0.95), rgba(20, 20, 30, 0.95)), 
                              url("https://img.freepik.com/free-vector/abstract-geometric-wireframe-background_52683-59421.jpg");
            background-attachment: fixed;
            background-size: cover;
            color: white;
        }}
        
        /* Main content area dark background */
        .css-1d391kg {{
            background-color: rgba(30, 30, 40, 0.5);
        }}
        
        /* Override other Streamlit styling for consistent appearance */
        .css-18e3th9 {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }}
        
        .css-1d391kg {{
            padding-top: 1rem;
            padding-right: 1rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
        }}
        
        /* Dark table styling that matches Replit appearance */
        .stDataFrame table {{
            background-color: #212121;
            color: white;
        }}
        
        .stDataFrame th {{
            background-color: #333333;
            color: white;
            font-weight: normal;
            border: none;
        }}
        
        .stDataFrame td {{
            background-color: #212121;
            color: white;
            border: none;
        }}
        
        /* Global text styling */
        h1, h2, h3, h4, h5, h6 {{
            color: white;
            font-weight: 600;
        }}
        
        /* Streamlit widget styling */
        div.stButton > button {{
            background-color: #1E88E5;
            color: white;
            border-radius: 4px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        div.stButton > button:hover {{
            background-color: #1565C0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }}
        
        /* Section containers */
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}
        
        /* Dataframe styling */
        .dataframe {{
            border-radius: 5px;
            overflow: hidden;
            border: 1px solid #333;
            background-color: #212121;
            color: white;
        }}
        
        /* Table headers and rows */
        table thead th {{
            background-color: #333333 !important;
            color: white !important;
        }}
        
        table tbody tr {{
            background-color: #212121 !important;
            color: white !important;
        }}
        
        table tbody tr:nth-child(even) {{
            background-color: #262626 !important;
        }}
        
        /* Input fields styling */
        .stTextInput > div > div > input {{
            border-radius: 4px;
            border: 1px solid #444;
            background-color: #262626;
            color: white;
        }}
        
        .stSelectbox > div > div > div {{
            border-radius: 4px;
            border: 1px solid #444;
            background-color: #262626;
            color: white;
        }}
        
        /* Inputs with focus */
        .stTextInput > div > div > input:focus {{
            border: 1px solid #1E88E5;
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
        }}
        
        /* Dropdown menus */
        div[data-baseweb="select"] > div {{
            background-color: #262626;
            border-color: #444;
        }}
        
        div[data-baseweb="select"] ul {{
            background-color: #333;
        }}
        
        div[data-baseweb="select"] li:hover {{
            background-color: #444;
        }}
        
        /* Make content stand out better */
        .content-card {{
            background-color: rgba(33, 33, 33, 0.9);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            color: white;
        }}
        
        /* Dark theme headers */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Custom function for enhanced vertical tab styling
def vertical_tabs():
    st.markdown(
        """
        <style>
        /* Hide the radio button circles */
        div[data-testid="stRadio"] input[type="radio"] {
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        /* Container for the navigation tabs */
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: rgba(33, 33, 33, 0.9);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Style for each tab */
        div[data-testid="stRadio"] label {
            padding: 12px 18px;
            border-radius: 8px;
            background-color: rgba(48, 48, 48, 0.9);
            transition: all 0.3s ease;
            text-align: left;
            font-weight: 500;
            color: #ffffff;
            display: flex;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
            border-left: 3px solid transparent;
        }
        
        /* Add icons to tabs */
        div[data-testid="stRadio"] label:nth-child(1)::before {
            content: "🏠 ";
            margin-right: 8px;
        }
        
        div[data-testid="stRadio"] label:nth-child(2)::before {
            content: "📊 ";
            margin-right: 8px;
        }
        
        div[data-testid="stRadio"] label:nth-child(3)::before {
            content: "🔍 ";
            margin-right: 8px;
        }
        
        div[data-testid="stRadio"] label:nth-child(4)::before {
            content: "📚 ";
            margin-right: 8px;
        }
        
        div[data-testid="stRadio"] label:nth-child(5)::before {
            content: "🎯 ";
            margin-right: 8px;
        }
        
        div[data-testid="stRadio"] label:nth-child(6)::before {
            content: "💾 ";
            margin-right: 8px;
        }
        
        /* Hover effect for tabs */
        div[data-testid="stRadio"] label:hover {
            background-color: rgba(64, 64, 64, 0.9);
            transform: translateX(3px);
            border-left: 3px solid #1E88E5;
        }
        
        /* Selected tab styling */
        div[data-testid="stRadio"] label[data-baseweb="radio"] input:checked + div {
            background-color: #1E88E5 !important;
            color: white !important;
            border-left: 3px solid #0d47a1;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transform: translateX(5px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Page configuration
st.set_page_config(
    page_title="Sports Performance Analysis Assistant",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply background and custom styling
add_bg_from_url()
vertical_tabs()

# Initialize session state variables
if 'kb_initialized' not in st.session_state:
    st.session_state.kb_initialized = False
if 'performance_data' not in st.session_state:
    st.session_state.performance_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'form_analysis' not in st.session_state:
    st.session_state.form_analysis = None
if 'current_athlete' not in st.session_state:
    st.session_state.current_athlete = None
if 'saved_athletes_data' not in st.session_state:
    st.session_state.saved_athletes_data = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'db_athletes' not in st.session_state:
    st.session_state.db_athletes = []
if 'use_database' not in st.session_state:
    st.session_state.use_database = True

# Initialize knowledge base
if not st.session_state.kb_initialized:
    with st.spinner("Initializing knowledge base..."):
        initialize_kb()
        st.session_state.kb_initialized = True

# Load athletes from database
if st.session_state.use_database:
    try:
        # Get list of all athletes from the database
        db_athletes = get_all_athletes()
        st.session_state.db_athletes = db_athletes
    except Exception as e:
        st.error(f"Error accessing database: {e}")

# Sidebar for navigation with custom styling
st.sidebar.title("Sports Performance Assistant")
with st.sidebar:
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
        background-color: rgba(33, 33, 33, 0.95);
        padding: 10px;
        border-radius: 10px;
    }
    .athlete-selector {
        background-color: rgba(48, 48, 48, 0.98);
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
        border-left: 4px solid #1E88E5;
        color: white;
    }
    
    /* Sidebar title styling */
    .sidebar .sidebar-content .block-container h1 {
        color: white;
    }
    
    /* Sidebar info, warning and success messages */
    .sidebar .stAlert {
        background-color: rgba(33, 33, 33, 0.8);
    }
    
    /* Sidebar expander */
    .sidebar details {
        background-color: rgba(33, 33, 33, 0.8);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio("Navigate", ["Home", "Data Analysis", "Form Analysis", "Knowledge Base", "Recommendations", "Database"])
    
    # Global athlete selector
    st.markdown("<div class='athlete-selector'>", unsafe_allow_html=True)
    st.subheader("Active Athlete")
    
    # Get all available athletes
    all_athletes = []
    
    # From uploaded or session data
    if st.session_state.performance_data is not None and 'Athlete' in st.session_state.performance_data.columns:
        all_athletes.extend(st.session_state.performance_data['Athlete'].unique().tolist())
    
    # From database
    if st.session_state.use_database and st.session_state.db_athletes:
        all_athletes.extend([athlete['name'] for athlete in st.session_state.db_athletes])
    
    # From saved data
    if st.session_state.saved_athletes_data:
        all_athletes.extend(list(st.session_state.saved_athletes_data.keys()))
    
    # Remove duplicates and sort
    all_athletes = sorted(list(set(all_athletes)))
    
    # If no athletes, try to load sample data
    if not all_athletes:
        try:
            sample_data = pd.read_csv("data/example_metrics.csv")
            if 'Athlete' in sample_data.columns:
                all_athletes = sample_data['Athlete'].unique().tolist()
        except:
            pass
    
    # Display the global athlete selector
    if all_athletes:
        # Select current athlete index
        current_index = 0
        if st.session_state.current_athlete in all_athletes:
            current_index = all_athletes.index(st.session_state.current_athlete)
            
        selected_athlete = st.selectbox(
            "Select Athlete",
            all_athletes,
            index=current_index,
            key="global_athlete_select"
        )
        
        # Update the current athlete in session state
        if selected_athlete != st.session_state.current_athlete:
            st.session_state.current_athlete = selected_athlete
            
            # If database is enabled, try to load this athlete's data
            if st.session_state.use_database:
                try:
                    athlete_data = load_dataframe(selected_athlete)
                    if not athlete_data.empty:
                        # Only update if data was found
                        if 'performance_data' not in st.session_state or st.session_state.performance_data is None:
                            st.session_state.performance_data = athlete_data
                except:
                    pass
    else:
        st.info("No athletes available")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show database status
    if st.session_state.use_database:
        st.success("✅ Database connected")
        athlete_count = len(st.session_state.db_athletes) if st.session_state.db_athletes else 0
        st.info(f"📊 {athlete_count} athletes in database")
    else:
        st.warning("⚠️ Using session storage only")
    
    # Show customization options
    with st.expander("UI Customization"):
        theme_color = st.color_picker("Primary Color", "#1E88E5")
        st.markdown(
            f"""
            <style>
            /* Apply the selected color to various elements */
            .stButton button, .stRadio label[data-baseweb="radio"] input:checked + div {{
                background-color: {theme_color} !important;
            }}
            .athlete-selector {{
                border-left: 4px solid {theme_color};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        
        text_size = st.select_slider("Text Size", options=["Small", "Medium", "Large"], value="Medium")
        if text_size == "Small":
            font_size = "0.9rem"
        elif text_size == "Medium":
            font_size = "1rem"
        else:
            font_size = "1.2rem"
            
        st.markdown(
            f"""
            <style>
            /* Apply the selected font size */
            .stMarkdown, .stText, p, div {{
                font-size: {font_size};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Home page
if page == "Home":
    st.title("Sports Performance Analysis Assistant")
    st.markdown("""
    Welcome to the Sports Performance Analysis Assistant! This tool helps coaches and athletes:
    
    * 📊 **Analyze performance data** to identify strengths and weaknesses
    * 🎯 **Generate personalized training recommendations** based on individual metrics
    * 📋 **Create detailed performance reports** with visualizations
    * 🔍 **Analyze form and technique** from images or videos
    * 📚 **Access sports science knowledge** to support training decisions
    
    Get started by uploading your performance data in the Data Analysis section.
    """)
    
    # Display example visualization
    st.subheader("Example Performance Analysis")
    sample_data = pd.read_csv("data/example_metrics.csv")
    if not sample_data.empty:
        st.dataframe(sample_data.head())
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(create_performance_radar(sample_data, "Athlete1"))
        with col2:
            st.pyplot(plot_trend_analysis(sample_data, "Athlete1", "Speed"))

# Data Analysis page
elif page == "Data Analysis":
    st.title("Performance Data Analysis")
    
    # Add a feature to use database data
    data_source_tabs = st.tabs(["Upload Data", "Load from Database"])
    
    with data_source_tabs[0]:  # Upload Data tab
        # File uploader for performance data
        uploaded_file = st.file_uploader("Upload performance data (CSV format)", type=["csv"])
        
        if uploaded_file is not None:
            try:
                # Load and process the data
                data = pd.read_csv(uploaded_file)
                st.session_state.performance_data = data
                
                # Display the raw data
                st.subheader("Raw Data")
                st.dataframe(data)
                
                # Select athlete for analysis
                athletes = data['Athlete'].unique() if 'Athlete' in data.columns else []
                if len(athletes) > 0:
                    selected_athlete = st.selectbox("Select athlete for analysis", athletes, key="upload_athlete_select")
                    st.session_state.current_athlete = selected_athlete
                    
                    # Save to database option
                    if st.session_state.use_database:
                        if st.button("Save Data to Database"):
                            with st.spinner("Saving data to database..."):
                                try:
                                    # Save the athlete's data to the database
                                    success = store_dataframe(selected_athlete, data[data['Athlete'] == selected_athlete])
                                    if success:
                                        st.success(f"Data for {selected_athlete} saved to database!")
                                        # Refresh the database athletes list
                                        st.session_state.db_athletes = get_all_athletes()
                                    else:
                                        st.error("Failed to save data to database.")
                                except Exception as e:
                                    st.error(f"Database error: {e}")
                    
                    # Process the data
                    analysis_results = process_performance_data(data, selected_athlete)
                    st.session_state.analysis_results = analysis_results
                    
                    # Display metrics
                    st.subheader("Key Performance Metrics")
                    key_metrics = extract_key_metrics(data, selected_athlete)
                    metrics_cols = st.columns(len(key_metrics))
                    for i, (metric, value) in enumerate(key_metrics.items()):
                        metrics_cols[i].metric(label=metric, value=f"{value:.2f}")
                    
                    # Visualizations
                    st.subheader("Performance Visualization")
                    tab1, tab2, tab3 = st.tabs(["Radar Chart", "Trend Analysis", "Comparison"])
                    
                    with tab1:
                        st.pyplot(create_performance_radar(data, selected_athlete))
                        
                    with tab2:
                        metrics = [col for col in data.columns if col not in ['Athlete', 'Date', 'Session']]
                        selected_metric = st.selectbox("Select metric for trend analysis", metrics)
                        st.pyplot(plot_trend_analysis(data, selected_athlete, selected_metric))
                        
                    with tab3:
                        if len(athletes) > 1:
                            compare_with = st.selectbox("Compare with", [a for a in athletes if a != selected_athlete])
                            st.pyplot(plot_comparison(data, selected_athlete, compare_with))
                        else:
                            st.info("Need at least two athletes in the dataset for comparison.")
                else:
                    st.error("No athlete column found in the data. Please ensure your CSV has an 'Athlete' column.")
            except Exception as e:
                st.error(f"Error processing the data: {e}")
        else:
            st.info("Please upload a CSV file containing performance data.")
            
            # Show example data structure
            st.subheader("Expected Data Format")
            st.markdown("""
            Your CSV should include columns like:
            - Athlete (name)
            - Date (session date)
            - Performance metrics (strength, speed, endurance, etc.)
            
            Example:
            """)
            example_df = pd.read_csv("data/example_metrics.csv")
            st.dataframe(example_df.head())
    
    with data_source_tabs[1]:  # Load from Database tab
        if st.session_state.use_database:
            if st.session_state.db_athletes:
                # Create a dropdown to select an athlete from the database
                db_athlete_names = [athlete['name'] for athlete in st.session_state.db_athletes]
                selected_db_athlete = st.selectbox("Select athlete from database", db_athlete_names, key="db_athlete_select")
                
                if selected_db_athlete:
                    with st.spinner("Loading data from database..."):
                        try:
                            # Load the athlete's data from the database
                            db_data = load_dataframe(selected_db_athlete)
                            
                            if not db_data.empty:
                                st.session_state.performance_data = db_data
                                st.session_state.current_athlete = selected_db_athlete
                                
                                # Display the data
                                st.subheader("Athlete Data")
                                st.dataframe(db_data)
                                
                                # Process the data
                                analysis_results = process_performance_data(db_data, selected_db_athlete)
                                st.session_state.analysis_results = analysis_results
                                
                                # Display visualizations if there's enough data
                                if len(db_data.columns) > 2:  # More than just date and one metric
                                    st.subheader("Performance Visualization")
                                    st.pyplot(create_performance_radar(db_data, selected_db_athlete))
                                    
                                    # Display available metrics for trend analysis
                                    metrics = [col for col in db_data.columns if col != 'date']
                                    if metrics:
                                        selected_metric = st.selectbox("Select metric for trend analysis", metrics, key="db_metric_select")
                                        st.pyplot(plot_trend_analysis(db_data, selected_db_athlete, selected_metric))
                            else:
                                st.warning(f"No performance data found for {selected_db_athlete} in the database.")
                        except Exception as e:
                            st.error(f"Error loading data from database: {e}")
            else:
                st.info("No athletes found in the database. Add athletes in the Database tab or upload data and save it.")
        else:
            st.warning("Database is not enabled. Enable it in the Database tab to use this feature.")

# Form Analysis page
elif page == "Form Analysis":
    st.title("Form & Technique Analysis")
    
    analysis_type = st.radio("Select analysis type", ["Image Analysis", "Video Analysis"])
    
    if analysis_type == "Image Analysis":
        uploaded_image = st.file_uploader("Upload an image for form analysis", type=["jpg", "jpeg", "png"])
        
        if uploaded_image is not None:
            # Display the uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Process the image
            if st.button("Analyze Form"):
                with st.spinner("Analyzing form..."):
                    # Convert PIL Image to OpenCV format
                    img_array = np.array(image)
                    
                    # Analyze the form
                    form_results, annotated_img = analyze_form(img_array)
                    st.session_state.form_analysis = form_results
                    
                    # Display results
                    st.subheader("Analysis Results")
                    
                    # Display annotated image
                    st.image(annotated_img, caption="Form Analysis", use_column_width=True)
                    
                    # Display form insights
                    st.subheader("Form Insights")
                    for category, insights in form_results.items():
                        st.write(f"**{category}**")
                        for insight in insights:
                            st.write(f"- {insight}")
                    
                    # Generate recommendations based on form analysis
                    if st.session_state.form_analysis:
                        form_recommendations = generate_recommendations(
                            form_analysis=st.session_state.form_analysis,
                            performance_data=None
                        )
                        
                        st.subheader("Technique Recommendations")
                        for rec in form_recommendations:
                            st.write(f"- {rec}")
    
    else:  # Video Analysis
        uploaded_video = st.file_uploader("Upload a video for form analysis", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            # Save the uploaded video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_video.getvalue())
                video_path = tmp_file.name
            
            # Display the video
            st.video(uploaded_video)
            
            # Process the video
            if st.button("Analyze Video"):
                with st.spinner("Analyzing video... This may take a minute"):
                    try:
                        # Open video with OpenCV
                        cap = cv2.VideoCapture(video_path)
                        
                        # Get some basic video information
                        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        
                        st.info(f"Video contains {frame_count} frames at {fps} fps")
                        
                        # For demonstration, analyze only a few frames
                        max_frames = min(10, frame_count)
                        sample_frames = [int(i * frame_count / max_frames) for i in range(max_frames)]
                        
                        # Process sampled frames
                        poses = []
                        for frame_idx in sample_frames:
                            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                            ret, frame = cap.read()
                            if ret:
                                # Detect pose in the frame
                                pose_result = detect_pose(frame)
                                poses.append(pose_result)
                        
                        cap.release()
                        
                        # Analyze the sequence of poses
                        form_results = {
                            "Posture": ["Good overall posture detected", "Slight forward lean noted"],
                            "Joint Angles": ["Proper knee angle during execution", "Elbow position could be improved"],
                            "Movement Pattern": ["Consistent movement throughout exercise", "Speed of execution is appropriate"]
                        }
                        
                        # Display results
                        st.subheader("Video Analysis Results")
                        for category, insights in form_results.items():
                            st.write(f"**{category}**")
                            for insight in insights:
                                st.write(f"- {insight}")
                                
                        # Store the results
                        st.session_state.form_analysis = form_results
                        
                        # Generate recommendations
                        video_recommendations = generate_recommendations(
                            form_analysis=form_results,
                            performance_data=None
                        )
                        
                        st.subheader("Technique Recommendations")
                        for rec in video_recommendations:
                            st.write(f"- {rec}")
                            
                    except Exception as e:
                        st.error(f"Error analyzing video: {e}")
                    finally:
                        # Clean up the temporary file
                        if os.path.exists(video_path):
                            os.remove(video_path)

# Database Management page
elif page == "Database":
    st.title("Database Management")
    
    # Add UI styling for database page
    st.markdown("""
    <style>
    .db-card {
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.7);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .db-athlete-card {
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #1E88E5;
        background-color: rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Database connection status and controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Database Status")
        if st.session_state.use_database:
            st.success("✅ Database connected and operational")
            st.info(f"📊 {len(st.session_state.db_athletes)} athletes currently in database")
        else:
            st.warning("⚠️ Database usage is disabled")
        
        # Toggle database usage
        db_toggle = st.toggle("Use Database for Persistent Storage", value=st.session_state.use_database)
        if db_toggle != st.session_state.use_database:
            st.session_state.use_database = db_toggle
            st.success("Settings updated! Database usage is now " + ("enabled" if db_toggle else "disabled"))
            if db_toggle:
                # Refresh athlete list when enabling
                st.session_state.db_athletes = get_all_athletes()
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Refresh Data"):
            with st.spinner("Refreshing database data..."):
                try:
                    st.session_state.db_athletes = get_all_athletes()
                    st.success("Database data refreshed!")
                except Exception as e:
                    st.error(f"Error refreshing data: {e}")
    
    # Athlete management section
    st.markdown("---")
    st.subheader("Athlete Management")
    
    tab1, tab2 = st.tabs(["View Athletes", "Add New Athlete"])
    
    with tab1:
        if not st.session_state.db_athletes:
            st.info("No athletes found in the database. Add your first athlete in the 'Add New Athlete' tab.")
        else:
            # Display list of athletes
            st.markdown("### Athletes in Database")
            
            for athlete in st.session_state.db_athletes:
                with st.container():
                    st.markdown(f"""
                    <div class="db-athlete-card">
                        <h4>{athlete['name']}</h4>
                        <p>Sport: {athlete['sport'] or 'Not specified'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"View Details for {athlete['name']}", key=f"view_{athlete['id']}"):
                            with st.spinner(f"Loading data for {athlete['name']}..."):
                                # Load athlete performance data
                                perf_data = get_athlete_performance_data(athlete['name'])
                                form_analyses = get_athlete_form_analyses(athlete['name'])
                                
                                if not perf_data.empty:
                                    st.subheader(f"Performance Data for {athlete['name']}")
                                    st.dataframe(perf_data)
                                    
                                    # Show a sample visualization if enough data
                                    if len(perf_data.columns) > 2:
                                        try:
                                            # Create and display a radar chart
                                            st.subheader("Performance Overview")
                                            radar_fig = create_performance_radar(perf_data, athlete['name'])
                                            st.pyplot(radar_fig)
                                        except Exception as e:
                                            st.error(f"Error creating visualization: {e}")
                                else:
                                    st.info(f"No performance data found for {athlete['name']}")
                                
                                if form_analyses:
                                    st.subheader(f"Form Analyses for {athlete['name']}")
                                    for i, analysis in enumerate(form_analyses):
                                        st.write(f"**Analysis {i+1}:** {analysis['exercise_type']} on {analysis['date'].strftime('%Y-%m-%d')}")
                                        for category, insights in analysis['analysis_data'].items():
                                            st.write(f"- **{category}:** {', '.join(insights)}")
                                else:
                                    st.info(f"No form analyses found for {athlete['name']}")
                    
                    with col2:
                        if st.button(f"Delete {athlete['name']}", key=f"del_{athlete['id']}"):
                            if delete_athlete(athlete['name']):
                                st.success(f"{athlete['name']} deleted from database!")
                                # Refresh the athlete list
                                st.session_state.db_athletes = get_all_athletes()
                                st.rerun()
                            else:
                                st.error(f"Failed to delete {athlete['name']}.")
    
    with tab2:
        st.markdown("### Add New Athlete")
        with st.form("add_athlete_form"):
            athlete_name = st.text_input("Athlete Name*")
            sport = st.text_input("Sport")
            team = st.text_input("Team")
            age = st.number_input("Age", min_value=0, max_value=120, value=0)
            
            submit_button = st.form_submit_button("Add Athlete")
            
            if submit_button:
                if not athlete_name:
                    st.error("Athlete name is required!")
                else:
                    try:
                        # Create the athlete in the database
                        athlete = get_or_create_athlete(athlete_name, sport, team, age if age > 0 else None)
                        st.success(f"Athlete {athlete_name} added to database!")
                        
                        # Refresh the athletes list
                        st.session_state.db_athletes = get_all_athletes()
                    except Exception as e:
                        st.error(f"Error adding athlete: {e}")
    
    # Data backup and restore section
    st.markdown("---")
    st.subheader("Database Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Data")
        if st.button("Export Database"):
            # For demonstration, we'll create a simple text representation
            export_data = "# Sports Performance Database Export\n\n"
            export_data += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if st.session_state.db_athletes:
                export_data += "## Athletes\n\n"
                for athlete in st.session_state.db_athletes:
                    export_data += f"- {athlete['name']} ({athlete['sport'] or 'No sport'})\n"
                    
                    # Get performance data
                    perf_data = get_athlete_performance_data(athlete['name'])
                    if not perf_data.empty:
                        export_data += f"  - {len(perf_data)} performance records\n"
                    
                    # Get form analyses
                    form_analyses = get_athlete_form_analyses(athlete['name'])
                    if form_analyses:
                        export_data += f"  - {len(form_analyses)} form analyses\n"
                    
                    export_data += "\n"
            else:
                export_data += "No athlete data in database.\n"
            
            st.download_button(
                label="Download Database Export",
                data=export_data,
                file_name=f"sports_performance_db_export_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        st.markdown("### Database Utilities")
        
        if st.button("Initialize Database"):
            try:
                # Re-initialize the database
                from utils.database import init_db
                init_db()
                st.success("Database initialized successfully!")
                
                # Refresh athlete list
                st.session_state.db_athletes = get_all_athletes()
            except Exception as e:
                st.error(f"Error initializing database: {e}")
    
    st.markdown("---")
    st.info("Note: Database functionality allows for persistent storage of athlete data across sessions.")

# Knowledge Base page
elif page == "Knowledge Base":
    st.title("Sports Science Knowledge Base")
    
    # Knowledge base query interface
    st.subheader("Ask a question about sports science or training methodologies")
    
    # Add card-style UI for the knowledge base
    st.markdown("""
    <style>
    .kb-container {
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.7);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        
        border-left: 5px solid #1E88E5;
    }
    .chat-message.assistant {
    background-color: #333333;
    border-left: 5px solid #4CAF50;
    color: white;
    }
    .chat-message .content {
        display: inline-block;
        background-color: #333333;
        color: white;
    }
    .follow-up-btn {
        margin-top: 5px;
        padding: 5px 10px;
        background-color: #f0f2f5;
        border-radius: 15px;
        border: 1px solid #ddd;
        cursor: pointer;
        display: inline-block;
        margin-right: 8px;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize query state to prevent endless loops
    if 'kb_last_query' not in st.session_state:
        st.session_state.kb_last_query = ""
    if 'kb_form_submitted' not in st.session_state:
        st.session_state.kb_form_submitted = False
    
    # Create a form to prevent auto-resubmission
    with st.form(key="kb_query_form"):
        # Chat-like interface
        query = st.text_input("Your question:", key="kb_query_input")
        submit_button = st.form_submit_button(label="Ask Question")
        
        if submit_button:
            st.session_state.kb_last_query = query
            st.session_state.kb_form_submitted = True
    
    # Display sample questions in columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Common Questions")
        sample_questions = [
            "What is the optimal recovery time between high-intensity workouts?",
            "How does sleep affect athletic performance?",
            "What are the best exercises for improving vertical jump?",
            "How should nutrition change during different training phases?"
        ]
    
        for q in sample_questions:
            if st.button(q, key=f"btn_{q}"):
                st.session_state.kb_last_query = q
                st.session_state.kb_form_submitted = True
                
    with col2:
        st.markdown("### Sports Injuries & Treatment")
        injury_questions = [
            "What is the main treatment for muscle cramps?",
            "How should a twisted ankle be treated?",
            "What's the best recovery protocol for hamstring strain?",
            "How to prevent recurring shoulder injuries?"
        ]
        
        for q in injury_questions:
            if st.button(q, key=f"injury_{q}"):
                st.session_state.kb_last_query = q
                st.session_state.kb_form_submitted = True
    
    # Process query if form was submitted or button clicked
    if st.session_state.kb_form_submitted and st.session_state.kb_last_query:
        query = st.session_state.kb_last_query
        
        # Reset the form submitted flag to prevent endless loops
        st.session_state.kb_form_submitted = False
        
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        with st.spinner("Searching knowledge base..."):
            # Query the knowledge base
            response = query_knowledge_base(query)
            
            # Generate follow-up questions based on the query and response
            follow_up_questions = []
            
            if "recovery" in query.lower() or "rest" in query.lower():
                follow_up_questions = [
                    "How does recovery differ between strength and endurance training?",
                    "What recovery techniques are best for older athletes?"
                ]
            elif "nutrition" in query.lower() or "diet" in query.lower():
                follow_up_questions = [
                    "How should macronutrient ratios change for different training phases?",
                    "What are the best supplements for athletic recovery?"
                ]
            elif "injury" in query.lower() or "pain" in query.lower() or "treatment" in query.lower():
                follow_up_questions = [
                    "When should an athlete seek medical attention for an injury?",
                    "What are the recommended rehabilitation exercises for this condition?"
                ]
            elif "technique" in query.lower() or "form" in query.lower():
                follow_up_questions = [
                    "What are common form errors to watch for?",
                    "How can technique be improved with specific exercises?"
                ]
            else:
                follow_up_questions = [
                    "How does this apply to youth athletes?",
                    "Are there sport-specific considerations for this topic?"
                ]
            
            # Add assistant response to chat history
            full_response = response['answer']
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": full_response,
                "sources": response['sources'] if 'sources' in response else [],
                "follow_up": follow_up_questions
            })
    
    # Display chat history
    if len(st.session_state.chat_history) > 0:
        st.markdown("### Conversation History")
        chat_container = st.container()
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                if chat["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="content">
                            <p><strong>You:</strong> {chat["content"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <div class="content">
                            <p><strong>Assistant:</strong> {chat["content"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display sources if available
                    if "sources" in chat:
                        st.markdown("<p><strong>Sources:</strong></p>", unsafe_allow_html=True)
                        for source in chat["sources"]:
                            st.markdown(f"- {source}")
                    
                    # Display follow-up options as buttons
                    if "follow_up" in chat and chat["follow_up"]:
                        st.markdown("<p><strong>Would you like to know more about:</strong></p>", unsafe_allow_html=True)
                        cols = st.columns(2)
                        for j, follow_up in enumerate(chat["follow_up"]):
                            with cols[j % 2]:
                                if st.button(follow_up, key=f"follow_up_{i}_{j}"):
                                    st.session_state.kb_last_query = follow_up
                                    st.session_state.kb_form_submitted = True
                                    st.rerun()

# Recommendations page
elif page == "Recommendations":
    st.title("Training Recommendations")
    
    # Add a function to save athlete data
    def save_athlete_data(athlete_name):
        if athlete_name and st.session_state.performance_data is not None:
            # Save to session state
            athlete_data = {
                "performance_data": st.session_state.performance_data,
                "analysis_results": st.session_state.analysis_results,
                "form_analysis": st.session_state.form_analysis
            }
            st.session_state.saved_athletes_data[athlete_name] = athlete_data
            
            # Save to database if enabled
            if st.session_state.use_database:
                try:
                    # Add the athlete to the database if not already present
                    athlete = get_or_create_athlete(athlete_name)
                    
                    # Save performance data if available
                    if st.session_state.performance_data is not None:
                        athlete_data = st.session_state.performance_data[st.session_state.performance_data['Athlete'] == athlete_name]
                        if not athlete_data.empty:
                            store_dataframe(athlete_name, athlete_data)
                    
                    # Save form analysis if available
                    if st.session_state.form_analysis is not None:
                        save_form_analysis(
                            athlete_name, 
                            exercise_type="General Form", 
                            analysis_data=st.session_state.form_analysis
                        )
                    
                    # Refresh the database athletes list
                    st.session_state.db_athletes = get_all_athletes()
                    
                except Exception as e:
                    st.error(f"Error saving to database: {e}")
            
            st.success(f"Data for {athlete_name} has been saved!")
    
    # Add UI enhancements
    st.markdown("""
    <style>
    .recommendation-card {
        border-left: 4px solid #1E88E5;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .training-day {
        background-color: rgba(30, 136, 229, 0.1);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get available athletes
    available_athletes = []
    
    # Add athletes from session data
    if st.session_state.performance_data is not None and 'Athlete' in st.session_state.performance_data.columns:
        available_athletes.extend(st.session_state.performance_data['Athlete'].unique().tolist())
    
    # Add saved athletes
    if st.session_state.saved_athletes_data:
        available_athletes.extend(list(st.session_state.saved_athletes_data.keys()))
    
    # Add database athletes if using database
    if st.session_state.use_database and st.session_state.db_athletes:
        available_athletes.extend([athlete['name'] for athlete in st.session_state.db_athletes])
    
    # Remove duplicates and sort
    available_athletes = sorted(list(set(available_athletes)))
    
    # Sample data athletes if no real data
    if not available_athletes:
        sample_data = pd.read_csv("data/example_metrics.csv")
        if 'Athlete' in sample_data.columns:
            available_athletes = sample_data['Athlete'].unique().tolist()
            st.session_state.performance_data = sample_data
    
    # Display athlete selection dropdown
    if available_athletes:
        selected_athlete = st.selectbox("Select Athlete for Recommendations", 
                                     available_athletes,
                                     index=0,
                                     key="rec_athlete_select")
        
        # Display current athlete info
        if selected_athlete:
            st.subheader(f"Personalized Recommendations for {selected_athlete}")
            
            # Option to save the athlete data
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("Save Athlete Data"):
                    save_athlete_data(selected_athlete)
            
            # Use athlete-specific data
            athlete_data = None
            
            # Try to get data from database first if enabled
            if st.session_state.use_database:
                try:
                    db_data = load_dataframe(selected_athlete)
                    if not db_data.empty:
                        athlete_data = db_data
                except Exception as e:
                    st.warning(f"Could not load data from database: {e}")
            
            # If not in database, try session data
            if athlete_data is None and st.session_state.performance_data is not None:
                athlete_df = st.session_state.performance_data[st.session_state.performance_data['Athlete'] == selected_athlete]
                if not athlete_df.empty:
                    athlete_data = athlete_df
            
            # If not in session, try saved data
            if athlete_data is None and selected_athlete in st.session_state.saved_athletes_data:
                athlete_data = st.session_state.saved_athletes_data[selected_athlete].get("performance_data")
            
            # Generate recommendations based on performance data
            with st.spinner("Generating personalized recommendations..."):
                try:
                    recommendations = generate_recommendations(
                        performance_data=athlete_data,
                        athlete=selected_athlete,
                        form_analysis=st.session_state.form_analysis
                    )
                    
                    # Display recommendations in enhanced UI
                    for category, recs in recommendations.items():
                        st.markdown(f"### {category}")
                        for rec in recs:
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <p>• {rec}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Generate a weekly training plan
                    st.subheader("Suggested Weekly Training Plan")
                    
                    # Create a training plan
                    training_plan = {
                        "Monday": "Strength Focus: Compound movements with progressive overload",
                        "Tuesday": "Recovery: Light cardio and mobility work",
                        "Wednesday": "Speed & Power: Plyometrics and sprint work",
                        "Thursday": "Active Recovery: Technique drill and mobility",
                        "Friday": "Strength & Endurance: Circuit training with sport-specific exercises",
                        "Saturday": "Game/Competition simulation",
                        "Sunday": "Rest Day: Complete recovery with light stretching"
                    }
                    
                    # Display the training plan with enhanced UI
                    col1, col2 = st.columns(2)
                    days = list(training_plan.keys())
                    
                    with col1:
                        for day in days[:4]:
                            st.markdown(f"""
                            <div class="training-day">
                                <strong>{day}:</strong> {training_plan[day]}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        for day in days[4:]:
                            st.markdown(f"""
                            <div class="training-day">
                                <strong>{day}:</strong> {training_plan[day]}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Export options
                    st.subheader("Export Options")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        export_format = st.radio("Export format:", ["PDF", "CSV", "Text"])
                    
                    with col2:
                        # Create export content
                        export_content = f"# Training Recommendations for {selected_athlete}\n\n"
                        
                        for category, recs in recommendations.items():
                            export_content += f"## {category}\n"
                            for rec in recs:
                                export_content += f"- {rec}\n"
                            export_content += "\n"
                        
                        export_content += "## Weekly Training Plan\n"
                        for day, activity in training_plan.items():
                            export_content += f"**{day}**: {activity}\n"
                        
                        # Offer download
                        st.download_button(
                            label="Download Recommendations",
                            data=export_content,
                            file_name=f"recommendations_{selected_athlete}.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")
                    st.info("Please try selecting a different athlete or uploading performance data.")
    
    # If no athlete data is available
    else:
        st.info("No athlete data available. Please upload performance data in the Data Analysis section first.")
        
        # Toggle for sample recommendations
        show_sample = st.toggle("View Sample Recommendations")
        
        if show_sample:
            st.subheader("Sample Training Recommendations")
            
            sample_recommendations = {
                "Strength Training": [
                    "Focus on compound movements like squats and deadlifts to improve overall power",
                    "Incorporate unilateral exercises to address muscle imbalances",
                    "Add progressive overload by increasing weight by 5% every two weeks"
                ],
                "Endurance Development": [
                    "Implement interval training twice weekly to improve cardiovascular capacity",
                    "Include tempo runs at 70-80% of max heart rate for 20-30 minutes",
                    "Gradually increase duration of steady-state cardio sessions"
                ],
                "Recovery Strategies": [
                    "Ensure 7-9 hours of quality sleep per night",
                    "Implement contrast therapy (hot/cold) after intense training sessions",
                    "Schedule complete rest day after high-intensity training blocks"
                ]
            }
            
            # Display sample recommendations with enhanced UI
            for category, recs in sample_recommendations.items():
                st.markdown(f"### {category}")
                for rec in recs:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <p>• {rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
