FROM continuumio/miniconda3

MAINTAINER Benjamin Stewart <ben.gis.stewart@gmail.com>

VOLUME /mnt/work/input
VOLUME /mnt/work/output

# Install Linux build files for compiling Cython extensions
RUN apt-get update -y
RUN apt-get install python-dev apt-utils libc-dev linux-headers-amd64 gcc -y

# Install Anaconda
#RUN echo "export PATH=/root/anaconda2/bin:$PATH" > /etc/profile.d/conda.sh && \
#    /bin/bash /build3rd/Anaconda2-5.0.1-Linux-x86_64.sh -b && \
#    rm /build3rd/Anaconda2-5.0.1-Linux-x86_64.sh

RUN . ~/.bashrc

# Add Conda bin to the path
ENV PATH /usr/bin:/usr/local/bin:/root/anaconda2/bin:/opt/conda/bin:/opt/conda/envs/spfeasenv/bin:$PATH
ENV PYTHONPATH /root/anaconda2/envs/spfeasenv/lib/python2.7/site-packages:/opt/conda/envs/spfeasenv/lib/python2.7/site-packages:$PYTHONPATH

# Force to Python 2.7
RUN conda install python=2.7 -y

# Create a virtual environment
RUN conda create --name spfeasenv python=2.7 -y

#Install the GBDx library
VOLUME /build3rd
ADD /gbdx-task-interface/ /build3rd/gbdx-task-interface/
WORKDIR /build3rd/gbdx-task-interface/
RUN ["/bin/bash", "-c", "source activate spfeasenv && python setup.py build && python setup.py install"]

# Activate the virtual environment and install Anaconda libraries
#RUN ["/bin/bash", "-c", "source activate spfeasenv && conda install --name spfeasenv certifi -y"] 
RUN ["/bin/bash", "-c", "source activate spfeasenv && pip install geopandas"] 
#RUN ["/bin/bash", "-c", "source activate spfeasenv && conda install --name spfeasenv -c conda-forge geopandas -y"] 
RUN ["/bin/bash", "-c", "source activate spfeasenv && conda install --name spfeasenv rasterio -y"] 

ADD /SampleData/ /mnt/work/input

WORKDIR /root

COPY ./run_spfeas_Zonal.py .
RUN chmod +x run_spfeas_Zonal.py

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["source activate spfeasenv && exec python run_spfeas_Zonal.py"]
