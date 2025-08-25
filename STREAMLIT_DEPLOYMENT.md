# 🎵 MusiPy Streamlit Deployment Guide

This guide will help you deploy the Streamlit version of MusiPy on various platforms.

## 🚀 Quick Start

### Local Development

```bash
# Install Streamlit dependencies
pip install -r requirements_streamlit.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment

1. **Push to GitHub** (if not already done)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Configure deployment:**
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.11
   - **Requirements file**: `requirements_streamlit.txt`

## 📁 File Structure for Streamlit

```
musipy_by_jennwang/
├── streamlit_app.py              # Main Streamlit application
├── requirements_streamlit.txt    # Streamlit-specific dependencies
├── app/                          # Flask app (original)
├── data/                         # Data files
├── models/                       # ML models
└── STREAMLIT_DEPLOYMENT.md       # This guide
```

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended)

**Pros:**
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Easy setup
- ✅ Built-in analytics

**Setup:**
```bash
# 1. Ensure your code is on GitHub
git add .
git commit -m "Add Streamlit version"
git push origin master

# 2. Go to share.streamlit.io
# 3. Deploy with these settings:
#    - Repository: wangjenn/musipy_by_jennwang
#    - Branch: master
#    - Main file path: streamlit_app.py
```

### 2. Heroku

**Create `setup.sh`:**
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**Create `Procfile`:**
```
web: sh setup.sh && streamlit run streamlit_app.py
```

### 3. Docker (Streamlit Version)

**Create `Dockerfile.streamlit`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Run with Docker:**
```bash
docker build -f Dockerfile.streamlit -t musipy-streamlit .
docker run -p 8501:8501 musipy-streamlit
```

## 🔧 Configuration

### Environment Variables

```bash
# For Streamlit Cloud
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
```

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
```

## 📊 Features Comparison

| Feature | Flask Version | Streamlit Version |
|---------|---------------|-------------------|
| **UI** | HTML/CSS/JS | Python widgets |
| **Deployment** | Docker/Heroku | Streamlit Cloud |
| **Development** | Template-based | Code-first |
| **Interactivity** | Form-based | Real-time |
| **Audio Playback** | ✅ | ✅ |
| **Personality Input** | Forms | Sliders |
| **Recommendations** | Table view | Cards |

## 🎯 Streamlit Advantages

✅ **Faster Development**: No HTML/CSS needed  
✅ **Interactive Widgets**: Real-time sliders and buttons  
✅ **Easy Deployment**: One-click to Streamlit Cloud  
✅ **Better UX**: Modern, responsive interface  
✅ **Data Visualization**: Built-in charts and graphs  
✅ **Session Management**: Automatic state handling  

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements_streamlit.txt
   ```

2. **File Path Issues**
   ```python
   # Use absolute paths for data files
   BASE_DIR = os.path.abspath(os.path.dirname(__file__))
   ```

3. **Memory Issues**
   ```python
   # Use caching for large data
   @st.cache_data
   def load_data():
       # Your data loading code
   ```

4. **Streamlit Cloud Issues**
   - Check file paths are correct
   - Ensure requirements.txt is in root directory
   - Verify Python version compatibility

### Performance Optimization

```python
# Cache expensive operations
@st.cache_data
def load_data():
    return pd.read_csv('data/final.csv')

@st.cache_resource
def load_model():
    return joblib.load('models/knn.pkl')
```

## 📈 Monitoring

### Streamlit Cloud Analytics
- User sessions
- Page views
- Performance metrics
- Error tracking

### Custom Analytics
```python
# Track user interactions
if st.button("Get Recommendations"):
    # Log user action
    st.session_state.recommendations_requested = True
```

## 🔒 Security Considerations

1. **Data Privacy**: No personal data stored
2. **Model Security**: ML model is read-only
3. **Input Validation**: All inputs are validated
4. **Rate Limiting**: Consider adding for production

## 🚀 Production Checklist

- [ ] Test all features locally
- [ ] Verify data file paths
- [ ] Check model loading
- [ ] Test audio playback
- [ ] Validate personality inputs
- [ ] Deploy to Streamlit Cloud
- [ ] Monitor performance
- [ ] Set up analytics

## 🎵 Ready to Deploy!

Your Streamlit version is ready for deployment. The interface is more modern and user-friendly than the Flask version, with:

- **Interactive sliders** for personality input
- **Real-time recommendations** 
- **Audio playback** for songs
- **Beautiful UI** with cards and styling
- **Easy deployment** to Streamlit Cloud

Choose your deployment method and share your personality-based music recommendation system with the world! 🎵✨
