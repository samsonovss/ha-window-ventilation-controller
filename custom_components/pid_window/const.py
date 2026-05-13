"""Constants for PID Window Controller."""

DOMAIN = "pid_window"
CONF_NAME = "name"
CONF_TEMP_SENSOR = "temp_sensor"
CONF_COVER_ENTITY = "cover_entity"
CONF_OUTDOOR_SENSOR = "outdoor_sensor"
CONF_TARGET_TEMP = "target_temp"
CONF_KP = "kp"
CONF_KI = "ki"
CONF_KD = "kd"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_MIN_POSITION = "min_position"
CONF_MAX_POSITION = "max_position"
CONF_OUTDOOR_SUMMER_LIMIT = "outdoor_summer_limit"
CONF_OUTDOOR_LOCK_THRESHOLD = "outdoor_lock_threshold"
CONF_ENABLE_OUTDOOR_LOCK = "enable_outdoor_lock"

DEFAULT_NAME = "PID Window Controller"
DEFAULT_TARGET_TEMP = 24.0
DEFAULT_KP = 15.0
DEFAULT_KI = 0.2
DEFAULT_KD = 0.0
DEFAULT_UPDATE_INTERVAL = 60
DEFAULT_MIN_POSITION = 0
DEFAULT_MAX_POSITION = 100
DEFAULT_OUTDOOR_SUMMER_LIMIT = 24.0
DEFAULT_OUTDOOR_LOCK_THRESHOLD = 28.0
