/*#wm release config:*/
    Insert into WM_RELEASE_CONFIG_ARCHIVE (RELEASE_NAME,SPRINT_NAME,DROP_NO,ARTIFACT_TYPE,ARTIFACT_NAME,ARTIFACT_VERSION,
    VERSION_CONTROL_PATH,EXPORT_REQUIRED,BUILD_REQUIRED,BUILD_STATUS,LAST_EXPORT_TIMESTAMP,
    LAST_EXPORTED_BY,PROCESSING_STATUS,SOURCE_SERVER_ALIAS,NEW_ARTIFACT,PARENT_ARTIFACTS,ARTIFACT_PRECEDENCE,
    TARGET_SERVER_ALIAS,FOR_DEPLOYMENT,FOR_ROLLBACK,BACKUP_ARTIFACTNAME,ADDED_BY_USER,ARTIFACT_CONFIG_DETAILS,
    RELEASE_NOTES,ARTIFACT_SUBTYPE,LAST_BUILD_ID,LAST_BUILD_TIMESTAMP,BACKUP_VERSION,ACTION)
    (Select * From WM_RELEASE_CONFIG_BACKUP WHERE  LAST_BUILD_TIMESTAMP < add_months(sysdate, -6)
    and LAST_BUILD_TIMESTAMP is not null);
    
    DELETE From WM_RELEASE_CONFIG_BACKUP WHERE LAST_BUILD_TIMESTAMP < add_months(sysdate, -6);
    
    /*cache manager config:*/
    insert into CACHE_MANAGER_CONFIG_ARCHIVE (RELEASE_NAME,SPRINT_NAME,DROP_NO,ARTIFACT_TYPE,ARTIFACT_NAME,ACTION,
    CACHE_MANAGER_NAME,CACHE_NAME,
    ETERNAL,MAX_ELEMENTS_IN_MEMORY,TIME_TO_LIVE,TIME_TO_IDLE,OVERFLOW_TO_DISK,PERSIST_TO_DISK,MAX_ENTRIES_LOCAL_DISK)
    (select CACHE_MANAGER_CONFIG_BACKUP.RELEASE_NAME,CACHE_MANAGER_CONFIG_BACKUP.SPRINT_NAME,CACHE_MANAGER_CONFIG_BACKUP.DROP_NO,
    CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE,
    CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME, CACHE_MANAGER_CONFIG_BACKUP.ACTION,CACHE_MANAGER_CONFIG_BACKUP.CACHE_MANAGER_NAME,
    CACHE_MANAGER_CONFIG_BACKUP.CACHE_NAME,
    CACHE_MANAGER_CONFIG_BACKUP.ETERNAL,CACHE_MANAGER_CONFIG_BACKUP.MAX_ELEMENTS_IN_MEMORY,CACHE_MANAGER_CONFIG_BACKUP.TIME_TO_LIVE,
    CACHE_MANAGER_CONFIG_BACKUP.TIME_TO_IDLE,
    CACHE_MANAGER_CONFIG_BACKUP.OVERFLOW_TO_DISK,CACHE_MANAGER_CONFIG_BACKUP.PERSIST_TO_DISK,CACHE_MANAGER_CONFIG_BACKUP.MAX_ENTRIES_LOCAL_DISK
    from CACHE_MANAGER_CONFIG_BACKUP Inner join WM_RELEASE_CONFIG
    On (WM_RELEASE_CONFIG.RELEASE_NAME = CACHE_MANAGER_CONFIG_BACKUP.RELEASE_NAME
    and WM_RELEASE_CONFIG.Sprint_name = CACHE_MANAGER_CONFIG_BACKUP.sprint_name
    and WM_RELEASE_CONFIG.DROP_NO = CACHE_MANAGER_CONFIG_BACKUP.DROP_NO
    and WM_RELEASE_CONFIG.ARTIFACT_TYPE = CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE
    and WM_RELEASE_CONFIG.ARTIFACT_NAME = CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME
    and WM_RELEASE_CONFIG.ACTION = CACHE_MANAGER_CONFIG_BACKUP.ACTION)
    where (WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP < add_months(sysdate, -6)
    and WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP is not null));
    
    DELETE (select * from CACHE_MANAGER_CONFIG_BACKUP INNER JOIN WM_RELEASE_CONFIG
    On (WM_RELEASE_CONFIG.RELEASE_NAME = CACHE_MANAGER_CONFIG_BACKUP.RELEASE_NAME
    and WM_RELEASE_CONFIG.Sprint_name = CACHE_MANAGER_CONFIG_BACKUP.sprint_name
    and WM_RELEASE_CONFIG.DROP_NO = CACHE_MANAGER_CONFIG_BACKUP.DROP_NO
    and WM_RELEASE_CONFIG.ARTIFACT_TYPE = CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE
    and WM_RELEASE_CONFIG.ARTIFACT_NAME = CACHE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME
    and WM_RELEASE_CONFIG.ACTION = CACHE_MANAGER_CONFIG_BACKUP.ACTION)
    where (WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP < add_months(sysdate, -6)));
    
    /*keyStore manager config:*/
    insert into KS_MANAGER_CONFIG_ARCHIVE (RELEASE_NAME,SPRINT_NAME,DROP_NO,ARTIFACT_TYPE,ARTIFACT_NAME,ACTION,KEYSTORE_NAME,
    KEYSTORE_DESCRIPTION,KEYSTORE_TYPE,KEYSTORE_PROVIDER,KEYSTORE_TARGET_FILE_NAME,KEYSTORE_TARGET_FILE_PATH)
    (select KEYSTORE_MANAGER_CONFIG_BACKUP.RELEASE_NAME,KEYSTORE_MANAGER_CONFIG_BACKUP.SPRINT_NAME,
    KEYSTORE_MANAGER_CONFIG_BACKUP.DROP_NO,KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE,
    KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME,KEYSTORE_MANAGER_CONFIG_BACKUP.ACTION,KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_NAME,
    KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_DESCRIPTION,
    KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_TYPE,KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_PROVIDER,
    KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_TARGET_FILE_NAME,KEYSTORE_MANAGER_CONFIG_BACKUP.KEYSTORE_TARGET_FILE_PATH
    from KEYSTORE_MANAGER_CONFIG_BACKUP Inner join WM_RELEASE_CONFIG
    On (WM_RELEASE_CONFIG.RELEASE_NAME = KEYSTORE_MANAGER_CONFIG_BACKUP.RELEASE_NAME
    and WM_RELEASE_CONFIG.Sprint_name = KEYSTORE_MANAGER_CONFIG_BACKUP.sprint_name
    and WM_RELEASE_CONFIG.DROP_NO = KEYSTORE_MANAGER_CONFIG_BACKUP.DROP_NO
    and WM_RELEASE_CONFIG.ARTIFACT_TYPE = KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE
    and WM_RELEASE_CONFIG.ARTIFACT_NAME = KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME
    and WM_RELEASE_CONFIG.ACTION = KEYSTORE_MANAGER_CONFIG_BACKUP.ACTION)
    where (WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP < add_months(sysdate, -6)
    and WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP is not null));
   
    DELETE (select * from KEYSTORE_MANAGER_CONFIG_BACKUP INNER JOIN WM_RELEASE_CONFIG
    On (WM_RELEASE_CONFIG.RELEASE_NAME = KEYSTORE_MANAGER_CONFIG_BACKUP.RELEASE_NAME
    and WM_RELEASE_CONFIG.Sprint_name = KEYSTORE_MANAGER_CONFIG_BACKUP.sprint_name
    and WM_RELEASE_CONFIG.DROP_NO = KEYSTORE_MANAGER_CONFIG_BACKUP.DROP_NO
    and WM_RELEASE_CONFIG.ARTIFACT_TYPE = KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_TYPE
    and WM_RELEASE_CONFIG.ARTIFACT_NAME = KEYSTORE_MANAGER_CONFIG_BACKUP.ARTIFACT_NAME
    and WM_RELEASE_CONFIG.ACTION = KEYSTORE_MANAGER_CONFIG_BACKUP.ACTION)
    where (WM_RELEASE_CONFIG.LAST_BUILD_TIMESTAMP < add_months(sysdate, -6)));
  
    
    
    /*wm release log: */
    insert into WM_RELEASE_LOG_ARCHIVE (RELEASE_NAME,SPRINT_NAME,ARTIFACT_TYPE,ARTIFACT_NAME,ARTIFACT_VERSION,
    ACTION_TYPE,ACTION_TIMESTAMP,USERNAME,PROCESSING_STATUS,MESSAGE,TARGET_ALIAS)
    (Select * From WM_RELEASE_LOG_BACKUP WHERE ACTION_TIMESTAMP < add_months(sysdate, -6)
    and ACTION_TIMESTAMP is not null);
    
    DELETE From WM_RELEASE_LOG_BACKUP WHERE (ACTION_TIMESTAMP < add_months(sysdate, -6));
    
    
    
    /*USER_GRP_ACL_MANAGER_BAKUP*/
    
    insert into USER_GRP_ACL_MANAGER_ARCHIVE (ID,RELEASE_NAME,SPRINT_NAME,BUILD_REQUIRED,BUILD_STATUS,
    TARGET_SERVER_ALIAS,ACTION,ARTIFACT_TYPE,USERNAME,GROUPNAME,ACL_NAME,ACL_SERVICE,ADDED_BY_USER,STATUS,
    ERROR_MESSAGE,FOR_DEPLOYMENT,ROLLBACK_ID,LAST_BUILD_TIMESTAMP,LAST_BUILD_ID)
    (SELECT * FROM USER_GRP_ACL_MANAGER_BACKUP WHERE LAST_BUILD_TIMESTAMP < add_months(sysdate, -6) and LAST_BUILD_TIMESTAMP is not null);
    
    DELETE From USER_GRP_ACL_MANAGER_BACKUP  WHERE LAST_BUILD_TIMESTAMP < add_months(sysdate, -6);
    
    
    
    /*CONNECTION_MANAGER*/
    
    insert into CONNECTION_MANAGER_ARCHIVE (ID,RELEASE_NAME,SPRINT_NAME,ENVIRONMENT,DB_ALIAS,ACTION,BUILD_REQUIRED,
    BUILD_STATUS,CONNECTION_ALIAS,SERVER_NAME,DATABASE_NAME,PORT,NETWORK_PROTOCOL,MINIMUM_POOL_SIZE,MAXIMUM_POOL_SIZE,
    POOL_INCREMENT_SIZE,BLOCKING_TIMEOUT,EXPIRE_TIMEOUT,STARTUP_RETRY_COUNT,STARTUP_BACKOFF_SECS,TRANSACTION_TYPE,
    ADDED_BY_USER,FOR_DEPLOYMENT,ROLLBACK_ID,LAST_BUILD_TIMESTAMP,LAST_BUILD_ID)
    (SELECT * FROM CONNECTION_MANAGER_BACKUP WHERE LAST_BUILD_TIMESTAMP < add_months(sysdate, -6) and LAST_BUILD_TIMESTAMP is not null);
    
    DELETE From CONNECTION_MANAGER_BACKUP  WHERE LAST_BUILD_TIMESTAMP < add_months(sysdate, -6);
    
    
  
END ARCHIVE_AND_PURGING;