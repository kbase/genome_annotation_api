FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer

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
