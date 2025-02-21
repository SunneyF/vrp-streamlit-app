# Use an official lightweight Python image.
FROM python:3.12-slim


# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY app/ ./app/

# Expose the port that Streamlit uses (default is 8501).
EXPOSE 8501

# Command to run the Streamlit app.
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
