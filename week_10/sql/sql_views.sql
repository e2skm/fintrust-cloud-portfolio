-- Includes v_daily_transfer_volume, v_volume_migration_progress and v_transfer_audit
CREATE OR REPLACE VIEW v_transfer_audit AS
SELECT v.volume_name, c.regulation, c.encryption_required, e.status AS execution_status, e.bytes_transferred, e.completed_at
FROM datasync_executions e
JOIN transfer_volumes v ON v.volume_id = e.task_id
LEFT JOIN compliance_requirements c ON c.volume_id = v.volume_id;