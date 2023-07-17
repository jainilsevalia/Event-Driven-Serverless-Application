# Use the official AWS Lambda Python runtime image
FROM public.ecr.aws/lambda/python:3.9

# Copy the Flask application code into the container
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

# Set the command to run the Flask application
CMD ["lambda_function.lambda_handler"]
