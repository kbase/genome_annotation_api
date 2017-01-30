FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

RUN sudo apt-get install python-dev libffi-dev libssl-dev
RUN pip install cffi --upgrade
RUN pip install pyopenssl --upgrade
RUN pip install ndg-httpsclient --upgrade
RUN pip install pyasn1 --upgrade
RUN pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade
RUN pip install --upgrade ndg-httpsclient

# update installed WS client (will now include get_objects2)
RUN mkdir -p /kb/module && \
    cd /kb/module && \
    git clone https://github.com/kbase/workspace_deluxe && \
    cd workspace_deluxe && \
    git checkout 837ad4c && \
    rm -rf /kb/deployment/lib/biokbase/workspace && \
    cp -vr lib/biokbase/workspace /kb/deployment/lib/biokbase/workspace

#install data_api
RUN mkdir -p /kb/module && \
    cd /kb/module && \
    git clone https://github.com/kbase/data_api -b 0.4.0-dev

RUN sed -i 's/six/#six/' /kb/module/data_api/requirements.txt && \
    pip install /kb/module/data_api

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
