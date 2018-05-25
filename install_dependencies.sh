#!/bin/bash
for dependency in $(cat $1)
do
  pip install $dependency
done
