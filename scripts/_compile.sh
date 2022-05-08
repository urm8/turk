#!/usr/bin/env bash
cd "$(git rev-parse --show-toplevel)" || exit 1
mkdir -p turk/proto
find turk/proto -type f -name '*.pyi' exec rm {} \;
python -m grpc_tools.protoc --proto_path="." --python_out=turk/proto --grpc_python_out=turk/proto --mypy_out=turk/proto $(find registry -type f -name '*.proto') && echo 'success' || echo 'fail ;(' && exit $?
