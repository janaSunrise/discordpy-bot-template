FROM python:3.8-slim

# Configure Pipenv for running in container
ENV PIPENV_HIDE_EMOJIS=1 \
    PIPENV_IGNORE_VIRTUALENVS=1 \
    PIPENV_NOSPIN=1 \
    PIPENV_NO_CACHE_DIR=false

# Get the dependencies ready
RUN apt-get -y update \
    && apt-get install git netcat -y \
    && rm -rf /root/.cache/pip/* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Define the working directory
WORKDIR /bot

# Copy all the files, and get dependencies ready
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy the source files
COPY . .

# Start the container
ENTRYPOINT ["sh"]
CMD ["wait-for-bot.sh"]
