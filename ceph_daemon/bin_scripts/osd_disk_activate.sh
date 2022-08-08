#!/bin/bash
set -e

function osd_activate {
  if [[ -z "${OSD_DEVICE}" ]] || [[ ! -b "${OSD_DEVICE}" ]]; then
    log "ERROR: you either provided a non-existing device or no device at all."
    log "You must provide a device to build your OSD ie: /dev/sdb"
    exit 1
  fi

  ulimit -Sn 1024
  ulimit -Hn 4096

  if [ -L "${OSD_DEVICE}" ]; then
    OSD_DEVICE=$(readlink -f "${OSD_DEVICE}")
  fi

  # check the DEVICE or lv(logical volume) if has ceph metadata info
  if [[ ! $(ceph-volume inventory ${OSD_DEVICE} |grep "osd id") ]]; then
    log "ERROR: ${OSD_DEVICE} doesn't have a ceph metadata partition"
    exit 1
  fi
  
  if [[ ${OSD_BLUESTORE} -eq 1 ]]; then
    # Find the OSD ID and the OSD FSID
    OSD_ID="$(ceph-volume inventory ${OSD_DEVICE} |grep "osd id" |awk '{print $3}')"
    OSD_FSID="$(ceph-volume inventory ${OSD_DEVICE} |grep "osd fsid" |awk '{print $3}')" 
    
    # Activate the OSD
    # Usage:
    # ceph-volume lvm activate --bluestore <osd id> <osd fsid>
    # or 
    # ceph-volume simple activate --bluestore <osd id> <osd fsid>
    if ceph-volume lvm activate --bluestore ${OSD_ID} ${OSD_FSID}; then
      log "INFO: Activate the OSD: osd.${OSD_ID} success"
    fi

  else
      data_part=$(dev_part "${OSD_DEVICE}" 1)

      if ! test -d /etc/ceph/osd || ! grep -q "${data_part}" /etc/ceph/osd/*.json; then
        log "INFO: Scanning ${data_part}"
        ceph-volume simple scan "${data_part}"
      fi

      CEPH_VOLUME_SCAN_FILE=$(grep -l "${data_part}" /etc/ceph/osd/*.json)

      # Find the OSD ID
      OSD_ID="$($PYTHON -c "import sys, json; print(json.load(sys.stdin)[\"whoami\"])" < "${CEPH_VOLUME_SCAN_FILE}")"

      # Activate the OSD
      # The command can fail so if it does, let's output the ceph-volume logs
      if ! ceph-volume simple activate --file "${CEPH_VOLUME_SCAN_FILE}" --no-systemd; then
        cat /var/log/ceph
        exit 1
      fi

  fi
  
  
  if [[ ${OSD_DMCRYPT} -eq 1 ]]; then
    umount_lockbox
  fi

  log "SUCCESS"
  # This ensures all resources have been unmounted after the OSD has exited
  # We define `sigterm_cleanup_post` here because:
  # - we want to 'protect' the following `exec` in particular.
  # - having the cleaning code just next to the concerned function in the same file is nice.
  function sigterm_cleanup_post {
    local ceph_mnt
    ceph_mnt="/var/lib/ceph/osd/${CLUSTER}-${OSD_ID}"
    log "osd_disk_activate: Unmounting $ceph_mnt"
    umount "$ceph_mnt" || (log "osd_disk_activate: Failed to umount $ceph_mnt"; lsof "$ceph_mnt")
  }
  # /usr/lib/systemd/system/ceph-osd@.service
  # LimitNOFILE=1048576
  # LimitNPROC=1048576
  ulimit -n 1048576 -u 1048576
  # start OSD
  exec /usr/bin/ceph-osd "${DAEMON_OPTS[@]}" -i "${OSD_ID}"
}
