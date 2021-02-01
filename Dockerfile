FROM kbase/sdkbase2:python
LABEL maintainer="scanon"
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


COPY ./ /kb/module

WORKDIR /kb/module

RUN mkdir -p /kb/module/work && \
    chmod -R a+rw /kb/module && \
    make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
