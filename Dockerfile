FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# update security libraries in the base image
RUN pip install setuptools --upgrade\
    && pip install cffi --upgrade \
    && pip install cryptography==1.9 \
    && pip install pyopenssl --upgrade \
    && pip install ndg-httpsclient --upgrade \
    && pip install pyasn1 --upgrade \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade #

# Install the data_api dependencies.  The code is directly copied into this repo
# right now so we can make hotfixes
RUN git clone https://github.com/kbase/data_api && \
    cd data_api && \
    git checkout 0.4.1-dev && \
    pip install thrift && \
    pip install -r requirements.txt && \
    rm -rf /kb/module/data_api

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
