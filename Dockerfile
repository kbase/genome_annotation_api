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
COPY ./lib/doekbase/requirements.txt /kb/module/requirements.txt
RUN pip install -r /kb/module/requirements.txt

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
