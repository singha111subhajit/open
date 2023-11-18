USE [master]
/*GO
** Object:  StoredProcedure [dbo].[DW_VMN_SELLING_TITLES]    Script Date: 08/04/2016 15:21:48 **
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
*/

  -- Populate the External Integer values for networks
  INSERT INTO WO_GUID_TO_EXTERNAL_INTEGERS
  (GUID_TO_EXTERNAL_INTEGER_ID)
  SELECT WO_STATIONS.STATION_ID
  FROM WO_STATIONS WITH (NOLOCK)
  LEFT OUTER JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI WITH (NOLOCK) ON WO_STATIONS.STATION_ID = GTEI.GUID_TO_EXTERNAL_INTEGER_ID
  WHERE GTEI.GUID_TO_EXTERNAL_INTEGER_ID IS NULL

  -- Populate the External Integer values for inventory codes
  INSERT INTO WO_GUID_TO_EXTERNAL_INTEGERS
  (GUID_TO_EXTERNAL_INTEGER_ID)
  SELECT WO_INVENTORY_CODES.INVENTORY_CODE_ID
  FROM WO_INVENTORY_CODES WITH (NOLOCK)
  LEFT OUTER JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI WITH (NOLOCK) ON WO_INVENTORY_CODES.INVENTORY_CODE_ID = GTEI.GUID_TO_EXTERNAL_INTEGER_ID
  WHERE GTEI.GUID_TO_EXTERNAL_INTEGER_ID IS NULL

  -- Populate the External Integer values for channel inventory codes
  INSERT INTO WO_GUID_TO_EXTERNAL_INTEGERS
  (GUID_TO_EXTERNAL_INTEGER_ID)
  SELECT WO_CHANNEL_INVENTORY_CODES.CHANNEL_INVENTORY_CODE_ID
  FROM WO_CHANNEL_INVENTORY_CODES WITH (NOLOCK)
  LEFT OUTER JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI WITH (NOLOCK) ON WO_CHANNEL_INVENTORY_CODES.CHANNEL_INVENTORY_CODE_ID = GTEI.GUID_TO_EXTERNAL_INTEGER_ID
  WHERE GTEI.GUID_TO_EXTERNAL_INTEGER_ID IS NULL

  -- Populate the External Integer values for dayparts
  INSERT INTO WO_GUID_TO_EXTERNAL_INTEGERS
  (GUID_TO_EXTERNAL_INTEGER_ID)
  SELECT WO_LOOKUPS.LOOKUP_GUID
  FROM WO_LOOKUPS WITH (NOLOCK)
  LEFT OUTER JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI WITH (NOLOCK) ON WO_LOOKUPS.LOOKUP_GUID = GTEI.GUID_TO_EXTERNAL_INTEGER_ID
  WHERE GTEI.GUID_TO_EXTERNAL_INTEGER_ID IS NULL
  AND (WO_LOOKUPS.LOOKUP_TYPE = 'DAYPART')

  -- Send the formatted dataset
  SELECT CASE WHEN WOCNS_SELLING_NAMES.INVENTORY_CODE_INT IS NULL THEN GTEI4.EXTERNAL_INTEGER ELSE GTEI.EXTERNAL_INTEGER END AS SELL_ID,
          -- CASE WHEN WOCNS_SELLING_NAMES.INVENTORY_CODE_INT IS NULL THEN CIC.CHANNEL_INVENTORY_CODE_ID ELSE IC.INVENTORY_CODE_ID END AS SELL_GUID,
         --GTEI2.EXTERNAL_INTEGER AS NET_ID,
         WO_STATIONS.STATION_CALL_LETTERS,
         IC.INVENTORY_CODE_NAME,         
         --WO_STATIONS.STATION_ID AS NET_GUID,
         --4 AS TYPE_ID,
         --IC.UPDATE_BY AS CHG_USER,
         --IC.UPDATE_DATE AS CHG_DT,
         --NULL AS INCL_CODE,
         --NULL AS BNDRY_CODE,
         FLIGHTS.FLIGHT_START AS FRST_WK,
         FLIGHTS.FLIGHT_END AS LAST_WK,
         CASE WHEN IC.ROW_STATE = 2 THEN 'Y' ELSE 'N' END AS DEACTIVE_FLG,
         --GTEI.EXTERNAL_INTEGER AS S_OBJ_GROUP_ID,
         --1 AS SID_VERSION_NUMBER,
         --'N' AS MIRROR_FLAG,
         --'S' AS STD_EXCLUSIVE_RESERVE_IND,
         GTEI3.EXTERNAL_INTEGER AS DAYPART_ID,
         --NULL AS INVENTORY_RPT_PARENT_SELL_ID,
         --ISNULL(WOCNS_SELLING_NAMES.EXTERNAL_CODE, '') AS EXTERNAL_VALUE,
         WO_PROGRAMS.PROGRAM_EXTERNAL_ID,
         WO_PROGRAMS.PROGRAM_NAME,
         CASE WHEN WOCNS_SELLING_NAMES.INVENTORY_CODE_INT IS NULL THEN 'N' ELSE 'Y' END AS PLANNING_ELIGIBLE,
         CASE WHEN WOCNS_SELLING_NAMES.ORDER_RESTRICTED_START_TIME IS NULL THEN 0 ELSE (WOCNS_SELLING_NAMES.ORDER_RESTRICTED_START_TIME / 1000) - 21600 END AS START_TIME,
         CASE WHEN WOCNS_SELLING_NAMES.ORDER_RESTRICTED_END_TIME IS NULL THEN 86400 ELSE (WOCNS_SELLING_NAMES.ORDER_RESTRICTED_END_TIME / 1000) - 21600 END AS END_TIME,
         CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS IS NOT NULL THEN
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 1 = 1 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 2 = 2 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 4 = 4 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 8 = 8 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 16 = 16 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 32 = 32 THEN 'Y' ELSE 'N' END +
            CASE WHEN WOCNS_SELLING_NAMES.ELIGIBLE_WEEKDAYS & 64 = 64 THEN 'Y' ELSE 'N' END
        ELSE NULL
        END AS ELG_DAYS,
        CATEGORY.LOOKUP_DESCR as Type,
        IC.REPORTING_NAME
  FROM WO_INVENTORY_CODES IC WITH (NOLOCK)
  JOIN WO_LOOKUPS DAYPARTS WITH (NOLOCK) ON IC.DAYPART_INT = DAYPARTS.LOOKUP_INT AND DAYPARTS.LOOKUP_VALUE <> 'NCAE'
  JOIN WO_CHANNEL_INVENTORY_CODES CIC WITH (NOLOCK) ON IC.INVENTORY_CODE_INT = CIC.INVENTORY_CODE_INT
  JOIN WO_CHANNELS WITH (NOLOCK) ON WO_CHANNELS.CHANNEL_INT = CIC.CHANNEL_INT
  JOIN WO_STATIONS WITH (NOLOCK) ON WO_STATIONS.STATION_ID = WO_CHANNELS.STATION_ID
  LEFT OUTER JOIN WOCNS_SELLING_NAMES WITH (NOLOCK) ON IC.INVENTORY_CODE_INT = WOCNS_SELLING_NAMES.INVENTORY_CODE_INT
  LEFT OUTER JOIN
  ( SELECT
       MIN(START_DATE) + 1 - dbo.WOBroadCastWeekDay(MIN(START_DATE)) AS FLIGHT_START,
       MAX(END_DATE) + 1 - dbo.WOBroadCastWeekDay(MAX(END_DATE)) AS FLIGHT_END,
        SELLING_NAME_INT
     FROM WOCNS_SELLING_NAME_FLIGHTS
    WHERE IS_ACTIVE <> 0
    GROUP BY SELLING_NAME_INT) AS FLIGHTS ON FLIGHTS.SELLING_NAME_INT = WOCNS_SELLING_NAMES.SELLING_NAME_INT
  JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI  WITH (NOLOCK) ON IC.INVENTORY_CODE_ID  = GTEI.GUID_TO_EXTERNAL_INTEGER_ID
  JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI2 WITH (NOLOCK) ON WO_STATIONS.STATION_ID = GTEI2.GUID_TO_EXTERNAL_INTEGER_ID
  JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI3 WITH (NOLOCK) ON DAYPARTS.LOOKUP_GUID = GTEI3.GUID_TO_EXTERNAL_INTEGER_ID
  JOIN WO_GUID_TO_EXTERNAL_INTEGERS GTEI4 WITH (NOLOCK) ON CIC.CHANNEL_INVENTORY_CODE_ID  = GTEI4.GUID_TO_EXTERNAL_INTEGER_ID
  JOIN WO_LOOKUPS CATEGORY on WOCNS_SELLING_NAMES.CATEGORY_INT=CATEGORY.LOOKUP_INT  AND CATEGORY.LOOKUP_TYPE='CNS_CATEGORY'
  LEFT OUTER JOIN WO_PROGRAMS WITH (NOLOCK) ON PROGRAM_INT = WOCNS_SELLING_NAMES.ORDER_PROGRAM_INT
  WHERE ((IC.IS_USED_IN_ORDERS = 1) OR (WOCNS_SELLING_NAMES.SELLING_NAME_ID IS NOT NULL))