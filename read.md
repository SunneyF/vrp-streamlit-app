vrp-streamlit-app/
├── app/
│   ├── vrp_solver.py         # Contains VRP solver using OR-Tools
│   └── streamlit_app.py      # The Streamlit app that visualizes the solution
├── tests/
│   └── test_vrp_solver.py    # Pytest tests for the solver
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── .github/
    └── workflows/
         └── ci-cd.yml        # GitHub Actions workflow file for CI/CD


docker build -t vrp-streamlit-app .
docker run -p 8501:8501 vrp-streamlit-app
http://localhost:8501

