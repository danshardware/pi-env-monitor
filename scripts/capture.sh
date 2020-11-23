#!/bin/bash

OUTDIR=${OUTDIR:=/var/pi-env/captures}

if [ ! -d "$OUTDIR" ]; then
	mkdir -p "$OUTDIR"
fi

DATECODE=$(date -u +"%Y-%m-%d_%H%M")
TSD_FILE="${OUTDIR}/tsd/${DATECODE}.tsd.json"

# capture an image and metadata
raspistill --nopreview --output "${OUTDIR}/${DATECODE}.jpg"
IMAGEMETA="{\"image\": \"${DATECODE}\"}"
curl -s http://localhost:8081/ | jq --compact-output ". + ${IMAGEMETA}" > "${OUTDIR}/${DATECODE}.json"
ln -sf "${OUTDIR}/${DATECODE}.jpg" "${OUTDIR}/latest.jpg"
ln -sf "${OUTDIR}/${DATECODE}.json" "${OUTDIR}/latest.json"

# process the metadata
nice python3 /usr/local/bin/calculateTimeSeries.py -o "${TSD_FILE}" -i "${DATECODE}"
if [ -r "${TSD_FILE}" ]; then
	ln -s "${TSD_FILE}" "${OUTDIR}/tsd/latest.tsd.json" 
fi

# make thumbnails
python3 /usr/local/bin/makeThumbnail.py -d resized -s _64 -x 64 -y 64 "${OUTDIR}/${DATECODE}.jpg"
python3 /usr/local/bin/makeThumbnail.py -d resized -s _640 -x 640 -y 640 "${OUTDIR}/${DATECODE}.jpg"
python3 /usr/local/bin/makeThumbnail.py -d resized -s _1200 -x 1200 -y 1200 "${OUTDIR}/${DATECODE}.jpg"
