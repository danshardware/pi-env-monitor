#!/bin/bash

OUTDIR=${OUTDIR:=/var/pi-env/captures}

if [ ! -d "$OUTDIR" ]; then
	mkdir -p "$OUTDIR"
fi

DATECODE=$(date -u +"%Y-%m-%d_%H%M")
raspistill --nopreview --output "${OUTDIR}/${DATECODE}.jpg"
curl -s http://localhost:8081/ -o "${OUTDIR}/${DATECODE}.json"
