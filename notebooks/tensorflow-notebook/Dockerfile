# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Selene Blok <selene.blok@gmail.com>"

RUN /opt/conda/bin/conda update -n root conda && \
    /opt/conda/bin/conda install -yq -c conda-forge psycopg2=2.7 && \
    /opt/conda/bin/conda clean -tipsy

# Install Tensorflow
RUN pip install --quiet \
    'tensorflow==2.1.0' && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
