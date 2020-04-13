# Get base image
FROM python:3.7-alpine

# Start working directory /mypro in the image
WORKDIR /mypro

# Copy all contents from current directory to /mypro directory in the image
COPY . /mypro

# Install all dependencies in the image mentioned in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8080 of the image
EXPOSE 8080

# When the image is turned into container then run this command to run the app
CMD ["python","app.py"]




Type a message

