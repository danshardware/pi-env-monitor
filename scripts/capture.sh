#!/bin/bash

OUTDIR=${OUTDIR:=/var/pi-env/captures}

if [ ! -d "$OUTDIR" ]; then
	mkdir -p "$OUTDIR"
fi

DATECODE=$(date -u +"%Y-%m-%d_%H%M")
TSD_FILE="${OUTDIR}/tsd/${DATECODE}.tsd.json"

raspistill --nopreview --output "${OUTDIR}/${DATECODE}.jpg"
curl -s http://localhost:8081/ -o "${OUTDIR}/${DATECODE}.json"
ln -sf "${OUTDIR}/${DATECODE}.jpg" "${OUTDIR}/latest.jpg"
ln -sf "${OUTDIR}/${DATECODE}.json" "${OUTDIR}/latest.json"
nice python3 /usr/local/bin/calculateTimeSeries.py -o "${TSD_FILE}" -i "${DATECODE}.jpg"
if [ -r "${TSD_FILE}" ]; then
	ln -s "${TSD_FILE}" "${OUTDIR}/tsd/latest.tsd.json" 
fi
