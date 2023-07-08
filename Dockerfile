FROM rasa/rasa:3.5.4-full


RUN pip install pandas
RUN pip install numpy


COPY . /app

# Train the Rasa model
RUN rasa train

# Expose the Rasa server port (default is 5005)
EXPOSE 5005

# Set the command to run the Rasa server when the container starts
CMD ["rasa", "run", "-m", "models", "--enable-api", "--cors", "*", "--debug"]
