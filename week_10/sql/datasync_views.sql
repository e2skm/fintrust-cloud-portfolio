CREATE OR REPLACE VIEW v_daily_transfer_volume AS
SELECT DATE(started_at) AS transfer_date,
       source_volume,
       COUNT(*) AS execution_count,
       SUM(files_transferred) AS total_files,
       ROUND(SUM(bytes_transferred)/1073741824.0,2) AS total_gb,
       SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) AS successful_runs,
       SUM(CASE WHEN status='ERROR' THEN 1 ELSE 0 END) AS failed_runs
FROM datasync_executions
GROUP BY DATE(started_at), source_volume
ORDER BY transfer_date DESC;

CREATE OR REPLACE VIEW v_volume_migration_progress AS
SELECT v.volume_name,
       v.source_system,
       v.total_size_gb,
       COALESCE(SUM(e.bytes_transferred)/1073741824.0,0) AS transferred_gb,
       ROUND(100.0 * COALESCE(SUM(e.bytes_transferred)/1073741824.0,0)/NULLIF(v.total_size_gb,0),1) AS pct_complete,
       MAX(e.completed_at) AS last_transfer
FROM transfer_volumes v
LEFT JOIN datasync_executions e ON v.volume_id=e.task_id AND e.status='SUCCESS'
GROUP BY v.volume_id,v.volume_name,v.source_system,v.total_size_gb
ORDER BY pct_complete DESC;

CREATE OR REPLACE VIEW v_transfer_audit AS
SELECT tv.volume_name,
       cr.regulation,
       cr.encryption_required,
       de.status AS execution_status,
       de.bytes_transferred,
       de.completed_at
FROM datasync_executions de
JOIN transfer_volumes tv ON de.task_id = tv.volume_id
JOIN compliance_requirements cr ON tv.volume_id = cr.volume_id;
