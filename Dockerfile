FROM docker:1.12

RUN apk add --update automake libtool m4 autoconf alpine-sdk linux-headers && \
    wget -qO- https://github.com/gmkurtzer/singularity/archive/2.1.2.tar.gz | tar zxv && \
    cd singularity-2.1.2 && ./autogen.sh && ./configure --prefix=/usr/local && make &&  make install && \
    cd ../ && rm -rf singularity-2.1.2 && \
    apk del automake libtool m4 autoconf alpine-sdk linux-headers

RUN mkdir -p /usr/local/var/singularity/mnt
RUN apk add e2fsprogs bash tar rsync bash python py-pip

ADD docker2singularity.sh /docker2singularity.sh
RUN chmod a+x /docker2singularity.sh

ADD agavepy/ /agavepy/
ADD d2s-varscript.py /d2s-varscript.py
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ARG user
ARG uid
ARG gid

RUN groupadd -g $gid G-$gid
RUN useradd --uid $uid --gid G-$gid --home-dir /home/$user --shell /bin/bash $user
USER $user 

CMD ["python", "/d2s-varscript.py"]
