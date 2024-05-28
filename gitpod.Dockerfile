# Use the official Gitpod full workspace image as the base image
FROM gitpod/workspace-full

# Install Graphviz
RUN sudo apt-get update && \
    sudo apt-get install -y graphviz
