#!/bin/bash

tail -n +2 data.txt | termgraph --title "Pie Sales (2020)" \
                                --width 40 \
                                --color magenta \
                                --format "{:.0f}" \
                                --no-labels
