#!/usr/bin/env bash
cd "$(git rev-parse --show-toplevel)" || exit 1
mkdir -p turk/proto
protoc --proto_path="." --python_out=turk/proto $(find registry -type f -name '*.proto') && echo 'success' || echo 'fail ;(' && exit $?