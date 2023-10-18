#!/bin/bash

source activate qiime2 && jupyter lab --allow-root --ip='*' --port=9000 --NotebookApp.token=$NB_PASSWORD --no-browser