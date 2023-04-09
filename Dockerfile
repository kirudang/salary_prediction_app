# Specify the base image for your Dockerfile
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file from project directory to the container's working directory
COPY requirements.txt ./requirements.txt

# Install the dependencies specified in the requirements.txt file using pip
RUN pip3 install -r requirements.txt

# Copy the rest of project files to the container's working directory
COPY . /app

# expose port
EXPOSE 8501:8051

# Set the entry point for the container to run the Streamlit web app
ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
#CMD ["sh","run.sh"]