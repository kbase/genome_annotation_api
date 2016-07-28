FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

RUN mkdir -p /kb/module && cd /kb/module && git clone https://github.com/kbase/data_api -b develop && \
    mkdir lib/

RUN pip install //kb/module/data_api
RUN pip install --upgrade ndg-httpsclient

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
