#!/usr/bin/env bash
set -e

jekyll build

aws2 s3 rm s3://blog.higashi.tech/ --recursive
aws2 s3 cp _site/ s3://blog.higashi.tech/ --recursive

echo "Upload Complete!"

