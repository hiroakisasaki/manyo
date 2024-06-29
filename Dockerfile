# Specify the base image
FROM python:3.9.6

# Install necessary packages
RUN apt-get update && apt-get install -y \
    mecab \
    fonts-noto-cjk \
    graphviz

# Install MeCab Python bindings
RUN pip install mecab-python3 graphviz

# Set the working directory
WORKDIR /usr/src/app

# Copy necessary files
COPY mecabrc /usr/local/etc/mecabrc
COPY mkhandic-mecab_0.2_bin /usr/local/lib/mecab/mkhandic-mecab_0.2_bin
COPY mecab.py /usr/src/app/mecab.py
COPY kanji_pron_dict.tsv /usr/src/app/kanji_pron_dict.tsv
COPY kanji_pron_gen.py /usr/src/app/kanji_pron_gen.py
COPY manyo_script.tsv /usr/src/app/manyo_script.tsv
COPY main.py /usr/src/app/main.py
COPY debug.py /usr/src/app/debug.py
COPY lattice.py /usr/src/app/lattice.py

# Set the entry point
# ENTRYPOINT ["python", "mecab.py"]
# ENTRYPOINT ["/bin/bash", "-c", "python /usr/src/app/mecab.py"]
ENTRYPOINT ["/bin/bash"]

# Expose port 8089
EXPOSE 8089

