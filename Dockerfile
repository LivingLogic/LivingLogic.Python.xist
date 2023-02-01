###
### Build stage
###

FROM python:3 as build-stage

WORKDIR /build

# Oracle Instant Client Version
ARG ORA_MAJOR=19
ARG ORA_MINOR=6

# Oracle Instant Client dependencies, `graphviz` for Sphinx diagram, and the rest for PDF generation
RUN apt-get update
RUN apt-get install -y \
  libaio1 \
  curl \
  wget \
  unzip \
  graphviz \
  latexmk \
  texlive \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended

# Install Oracle Instant Client binaries
RUN cd /tmp && \
    wget -q https://download.oracle.com/otn_software/linux/instantclient/${ORA_MAJOR}${ORA_MINOR}00/instantclient-basic-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    wget -q https://download.oracle.com/otn_software/linux/instantclient/${ORA_MAJOR}${ORA_MINOR}00/instantclient-sdk-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    wget -q https://download.oracle.com/otn_software/linux/instantclient/${ORA_MAJOR}${ORA_MINOR}00/instantclient-sqlplus-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    wget -q https://download.oracle.com/otn_software/linux/instantclient/${ORA_MAJOR}${ORA_MINOR}00/instantclient-tools-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    mkdir -p /opt/oracle && cd /opt/oracle && \
    unzip /tmp/instantclient-basic-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    unzip /tmp/instantclient-sdk-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    unzip /tmp/instantclient-tools-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    unzip /tmp/instantclient-sqlplus-linux.x64-${ORA_MAJOR}.${ORA_MINOR}.0.0.0dbru.zip && \
    echo /opt/oracle/instantclient_${ORA_MAJOR}_${ORA_MINOR} > /etc/ld.so.conf.d/oracle.conf && \
    ldconfig && \
    rm /tmp/*.zip

# Add Oracle Instant Client to the path
ENV PATH="/opt/oracle/instantclient_${ORA_MAJOR}_${ORA_MINOR}:${PATH}"

# Suppress pip version warning
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install modules required by XIST or for building the documentation
RUN pip install cssutils cx_Oracle CherryPy Sphinx sphinxcontrib.jquery pygll

# Pass version info into the container
ARG CI_COMMIT_TAG
ENV CI_COMMIT_TAG=$CI_COMMIT_TAG
ARG CI_COMMIT_REF_NAME
ENV CI_COMMIT_REF_NAME=$CI_COMMIT_REF_NAME
ARG CI_COMMIT_SHA
ENV CI_COMMIT_SHA=$CI_COMMIT_SHA
ARG CI_COMMIT_SHORT_SHA
ENV CI_COMMIT_SHORT_SHA=$CI_COMMIT_SHORT_SHA

# Copy everything into the container (as Sphinx autodoc needs XIST itself to be installed)
COPY . .

# Install XIST
RUN pip install -e .

# Build PDF
RUN cd docs && make doc

###
### Production stage
###

FROM nginx:alpine as production-stage
WORKDIR /usr/share/nginx/html
RUN apk --no-cache add curl
COPY --from=build-stage /build/docs/build/html /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=60s --timeout=3s --start-period=30s \
    CMD curl --fail -A "docker-healthcheck-curl" http://localhost:80/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
