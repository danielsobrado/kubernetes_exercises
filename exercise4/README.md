### Exercise 4: Scheduled Backup Job

**Task:**
Create a Kubernetes CronJob for database backups:

- The CronJob should be in the `backup` namespace.
- Name the CronJob `db-backup`.
- Use the `alpine` image.
- The job should run a script that echoes "Database backup completed" (simulating a backup process).
- Schedule the job to run at midnight every day (`0 0 * * *`).