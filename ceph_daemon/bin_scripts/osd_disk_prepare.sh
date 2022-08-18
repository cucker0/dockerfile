#!/bin/bash
set -e

function osd_disk_prepare {
  if [[ -z "${OSD_DEVICE}" ]];then
    log "ERROR- You must provide a device to build your OSD ie: /dev/sdb"
    exit 1
  fi

  if [[ ! -e "${OSD_DEVICE}" ]]; then
    log "ERROR- The device pointed by OSD_DEVICE ($OSD_DEVICE) doesn't exist !"
    exit 1
  fi

  if [ ! -e "$OSD_BOOTSTRAP_KEYRING" ]; then
    log "ERROR- $OSD_BOOTSTRAP_KEYRING must exist. You can extract it from your current monitor by running 'ceph auth get client.bootstrap-osd -o $OSD_BOOTSTRAP_KEYRING'"
    exit 1
  fi

  ceph_health client.bootstrap-osd "$OSD_BOOTSTRAP_KEYRING"
  
  # check the DEVICE or lv(logical volume) if has ceph metadata info
  # `ceph-volume inventory`
  # ref https://docs.ceph.com/en/latest/man/8/ceph-volume/#inventory
  if [[ $(ceph-volume inventory "${OSD_DEVICE}" |grep "not used by ceph") ]]; then
    log "INFO: ${OSD_DEVICE} is not available for use with ceph"
    return
  elif [[ $(ceph-volume inventory "${OSD_DEVICE}" |grep "osd id") ]]; then
    log "INFO: It looks like ${OSD_DEVICE} is an OSD" 
    return
  fi
  
  # clear all elements of CEPH_DISK_CLI_OPTS, then copy the array CLI_OPTS all elements to CEPH_DISK_CLI_OPTS
  IFS=" " read -r -a CEPH_DISK_CLI_OPTS <<< "${CLI_OPTS[*]}"
  if [[ ${OSD_DMCRYPT} -eq 1 ]]; then
    # We need to do a mapfile because ${OSD_LOCKBOX_UUID} needs to be quoted
    # so doing a regular CLI_OPTS+=("${OSD_LOCKBOX_UUID}") will make shellcheck unhappy.
    # Although the array can still be incremented by the others task using a regular += operator
    mapfile -t CEPH_DISK_CLI_OPTS_ARRAY <<< "${CEPH_DISK_CLI_OPTS[*]} --dmcrypt --lockbox-uuid ${OSD_LOCKBOX_UUID}"
    IFS=" " read -r -a CEPH_DISK_CLI_OPTS <<< "${CEPH_DISK_CLI_OPTS_ARRAY[*]}"
  fi
  
  # create OSD
  if [[ ${OSD_BLUESTORE} -eq 1 ]]; then
    CEPH_DISK_CLI_OPTS+=(--bluestore)
    CEPH_DISK_CLI_OPTS+=(--data "${OSD_DEVICE}")
    if [[ -n "${OSD_BLUESTORE_BLOCK_WAL}" && "${OSD_BLUESTORE_BLOCK_WAL}" != "${OSD_DEVICE}" ]]; then    
       CEPH_DISK_CLI_OPTS+=(--block.wal "${OSD_BLUESTORE_BLOCK_WAL}")
    fi
    if [[ -n "${OSD_BLUESTORE_BLOCK_DB}" && "${OSD_BLUESTORE_BLOCK_DB}" != "${OSD_DEVICE}" ]]; then
      CEPH_DISK_CLI_OPTS+=(--block.db "${OSD_BLUESTORE_BLOCK_DB}")
    fi
    #ceph-disk -v prepare "${CEPH_DISK_CLI_OPTS[@]}" \
    #--block-uuid "${OSD_BLUESTORE_BLOCK_UUID}" \
    #"${OSD_DEVICE}"
    
    # ceph-disk is Deprecated
    # use ceph-volume instead of ceph-disk. 
    # ref 
    # 语法：ceph-volume lvm prepare --bluestore --data <device> --block.wal <wal-device> --block.db <db-device>
    # --data  可以是使用 vg/lv 表示的逻辑卷。其它设备可以是现有的 逻辑卷 或 GPT分区。如果 --data 为 磁盘设备，则会自动创建 pv,vg,lv
    log "INFO: ceph-volume lvm prepare ${CEPH_DISK_CLI_OPTS[@]}"
    ceph-volume lvm prepare "${CEPH_DISK_CLI_OPTS[@]}"

  elif [[ "${OSD_FILESTORE}" -eq 1 ]]; then
    CEPH_DISK_CLI_OPTS+=(--filestore)
    CEPH_DISK_CLI_OPTS+=(--data "${OSD_DEVICE}")
    
    if [[ -n "${OSD_JOURNAL}" ]]; then
      #ceph-disk -v prepare "${CEPH_DISK_CLI_OPTS[@]}" --journal-uuid "${OSD_JOURNAL_UUID}" "${OSD_DEVICE}" "${OSD_JOURNAL}"
      ceph-volume lvm prepare "${CEPH_DISK_CLI_OPTS[@]}" --journal "${OSD_JOURNAL}"
    else
      #ceph-disk -v prepare "${CEPH_DISK_CLI_OPTS[@]}" --journal-uuid "${OSD_JOURNAL_UUID}" "${OSD_DEVICE}"
      log "ERROR: use FILESTORE you must provide OSD_JOURNAL"
    fi
  fi
    
  # 块设备加密的情况。dmcrypt -- Device Mapper crypt
  if [[ ${OSD_DMCRYPT} -eq 1 ]]; then
    # unmount lockbox partition when using dmcrypt
    umount_lockbox

    # close dmcrypt device
    # shellcheck disable=SC2034
    DATA_UUID=$(get_part_uuid "$(dev_part "${OSD_DEVICE}" 1)")
    # shellcheck disable=SC2034
    DATA_PART=$(dev_part "${OSD_DEVICE}" 1)
    if [[ ${OSD_BLUESTORE} -eq 1 ]]; then
      get_dmcrypt_bluestore_uuid
      close_encrypted_parts_bluestore
    elif [[ "${OSD_FILESTORE}" -eq 1 ]]; then
      get_dmcrypt_filestore_uuid
      close_encrypted_parts_filestore
    fi
  fi

  # watch the udev event queue, and exit if all current events are handled
  udevadm settle --timeout=600

  apply_ceph_ownership_to_disks
}
