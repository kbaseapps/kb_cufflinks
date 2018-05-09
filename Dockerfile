FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update && apt-get install -y sysstat

RUN pip install coverage \
    && pip install pathos

# ---------------------------------------------------------

# download Cufflinks software and untar it
ENV VERSION='2.2.1'
ENV DEST=/opt/cufflinks

RUN cd /opt && \
    mkdir -p $DEST && \
    wget "http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-${VERSION}.Linux_x86_64.tar.gz" && \
    tar -xzvf cufflinks-${VERSION}.Linux_x86_64.tar.gz && \
    rm cufflinks-${VERSION}.Linux_x86_64.tar.gz && \
    cd cufflinks-${VERSION}.Linux_x86_64 && \
	cp `find . -maxdepth 1 -perm -111 -type f` ${DEST} && \
	cd ../ && \
	rm -rf cufflinks-${VERSION}.Linux_x86_64

ENV PATH $PATH:${DEST}

# ---------------------------------------------------------

# Install gffread
RUN  echo Installing gffread \
  && cd /opt \
  && git clone https://github.com/gpertea/gclib \
  && git clone https://github.com/gpertea/gffread \
  && cd gffread \
  && make

ENV PATH $PATH:/opt/gffread

# ---------------------------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
