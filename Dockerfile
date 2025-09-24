###
### Build stage
###

FROM python:3 AS build-stage

WORKDIR /build

# Oracle Instant Client Version
ARG ORA_MAJOR=19
ARG ORA_MINOR=6

# Oracle Instant Client dependencies, `graphviz` for Sphinx diagram, and the rest for PDF generation
RUN apt-get update
RUN apt-get install -y \
  curl \
  graphviz \
  latexmk \
  texlive \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended

# Suppress pip version warning
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install modules required by XIST or for building the documentation
RUN pip install cssutils oracledb CherryPy Sphinx sphinxcontrib.jquery pygll

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

FROM nginx:alpine AS production-stage
WORKDIR /usr/share/nginx/html
RUN apk --no-cache add curl
COPY --from=build-stage /build/docs/build/html /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=60s --timeout=3s --start-period=30s \
    CMD curl --fail -A "docker-healthcheck-curl" http://localhost:80/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
