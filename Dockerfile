FROM python:3.6.9

WORKDIR /usr/src/app

COPY *.py ./
COPY requirements.txt .
COPY images.csv .
COPY images ./images/
COPY results ./results/

RUN pip install -r requirements.txt

# CMD [ "python", "./image_comparator.py" ]
ENTRYPOINT ["/bin/bash"]
