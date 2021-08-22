FROM continuumio/miniconda3

WORKDIR /graphBalancingConda
COPY . /graphBalancingConda

# Create the environment:
COPY graphB/env/linux_env.yml .
RUN conda env create -f linux_env.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "graphB", "/bin/bash", "-c"]

# Activate the environment, and make sure it's activated:
#RUN conda activate graphB

# The code to run when container is started:
COPY graphB/run.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "graphB", "bash", "./run.sh"]

