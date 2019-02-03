#!/usr/bin/env bash

case "${EXAMPLE_REGION}" in
    Tokyo)
        echo "${EXAMPLE_NAME} is recommended to visit Tokyo SkyTree ^_^"
        ;;
    Moscow)
        echo "${EXAMPLE_NAME} should visit the Red Square:)"
        ;;
    London)
        echo "${EXAMPLE_NAME} must take a look on the Tower!"
        ;;
    **)
        echo "${EXAMPLE_NAME} is in unknown place..."
        ;;
esac
bash
