-- Optional indexes to improve query performance
CREATE INDEX IF NOT EXISTS idx_production_device_time ON production_data (device_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_production_point ON production_data (point_name);
CREATE INDEX IF NOT EXISTS idx_events_device_time ON events (device_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_level ON events (level);

