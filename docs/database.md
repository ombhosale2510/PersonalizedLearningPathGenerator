# PostgreSQL and pgAdmin Setup

This document guides you through setting up and using PostgreSQL with pgAdmin for the Personalized Learning Path Generator project.

## PostgreSQL Configuration

### Database Setup

1. **Open pgAdmin**: Launch the pgAdmin application that you already have installed.

2. **Create a Database**:
   - Right-click on "Databases" in the left panel and select "Create" → "Database"
   - Name your database `personalized_learning_path`
   - Click "Save"

3. **Configure Connection in Project**:
   - The project's database connection is configured in `database.py` 
   - Update the connection string if needed:
   ```python
   DATABASE_URL = "postgresql://username:password@localhost:5432/personalized_learning_path"
   ```
   - Replace `username` and `password` with your PostgreSQL credentials

### Running Database Migrations

The project creates the necessary tables when it starts using SQLAlchemy's `Base.metadata.create_all(engine)`. This happens automatically in the `create_tables()` function in `app.py` which is called at application startup.

## Using pgAdmin

### Viewing Tables

After running the application for the first time, tables will be created automatically. To view them:

1. In pgAdmin, expand your `personalized_learning_path` database
2. Navigate to Schemas → public → Tables
3. You should see the following tables:
   - `users`
   - `courses`
   - `course_topics`
   - `enrollments`
   - `learning_paths`
   - `learning_path_items`

### Querying Data

pgAdmin provides an SQL editor to run queries:

1. Right-click on your database and select "Query Tool"
2. Write SQL queries to inspect or modify your data:

```sql
-- View all users
SELECT * FROM users;

-- View all courses
SELECT * FROM courses;

-- View courses with their topics
SELECT c.*, array_agg(ct.name) as topics
FROM courses c
LEFT JOIN course_topics ct ON c.id = ct.course_id
GROUP BY c.id;

-- View learning paths with associated courses
SELECT lp.*, lpi.order, c.title as course_title
FROM learning_paths lp
JOIN learning_path_items lpi ON lp.id = lpi.learning_path_id
JOIN courses c ON lpi.course_id = c.id
ORDER BY lp.id, lpi.order;
```

### Manually Adding Test Data

You can populate your database with test data using pgAdmin:

1. In the Query Tool, run the following SQL to add sample courses:

```sql
-- Add sample courses (Note: Use UPPERCASE for difficulty values since they're enum types)
INSERT INTO courses (title, description, difficulty, duration_hours, created_at)
VALUES 
('Introduction to Python', 'Learn Python fundamentals for beginners', 'BEGINNER', 10, NOW()),
('Web Development with JavaScript', 'Modern web development using JavaScript', 'INTERMEDIATE', 15, NOW()),
('Data Science Fundamentals', 'Introduction to data analysis and visualization', 'BEGINNER', 12, NOW()),
('Advanced Machine Learning', 'Deep learning and neural networks', 'ADVANCED', 20, NOW());

-- Add topics for the courses
INSERT INTO course_topics (course_id, name)
VALUES 
(1, 'Python'),
(1, 'Programming'),
(2, 'JavaScript'),
(2, 'Web Development'),
(2, 'HTML'),
(2, 'CSS'),
(3, 'Data Science'),
(3, 'Python'),
(3, 'Statistics'),
(4, 'Machine Learning'),
(4, 'Python'),
(4, 'Neural Networks');

-- Create a test user (password will be "password123")
INSERT INTO users (username, email, password_hash, created_at)
VALUES ('testuser', 'test@example.com', '$2b$12$tPBcLADdbWQgc1KwNbFjmej/P9dR2VYcMctI6Ap4MJQYia.zszxVa', NOW());
```

**IMPORTANT**: Note that the difficulty values in the SQL insert statement are in UPPERCASE ('BEGINNER', 'INTERMEDIATE', 'ADVANCED'). This is because the difficulty column is defined as an Enum type in the database model, and PostgreSQL requires you to use the enum names rather than values when inserting data.

## Backups and Maintenance

### Creating a Database Backup

1. Right-click on your database and select "Backup..."
2. Configure the backup options:
   - Format: Custom or Plain
   - Filename: Choose a location to save the backup file
   - Encoding: UTF8
3. Click "Backup" to create the backup file

### Restoring a Database

1. Right-click on your database and select "Restore..."
2. Select your backup file
3. Choose the appropriate format and options
4. Click "Restore" to restore your database

## Troubleshooting

### Connection Issues

If you're unable to connect to the database:

1. Verify PostgreSQL is running:
   - On Windows: Check Services to ensure PostgreSQL service is running
   - On Linux/Mac: Run `ps aux | grep postgres` to check if the process is active

2. Check credentials in `database.py`:
   - Ensure username and password are correct
   - Verify the port number (default is 5432)
   - Make sure the database name is correct

3. Test connection directly in pgAdmin:
   - Try connecting to the database using pgAdmin with the same credentials
   - If that works, the issue is likely in your application configuration

### Tables Not Created

If tables aren't being created automatically:

1. Check console output for any SQLAlchemy errors when the app starts
2. Verify that `create_tables()` is being called in `app.py`
3. Check that your models extend `Base` from `database.py`

### Data Insertion Errors

If you encounter errors when inserting data:

1. **Enum Type Values**: For columns with Enum types (like the `difficulty` column in the `courses` table), make sure to use the UPPERCASE enum names ('BEGINNER', 'INTERMEDIATE', 'ADVANCED') rather than the lowercase values.

2. **Constraints**: Check that your data meets any constraints defined in the database models (e.g., not null constraints, foreign key constraints, etc.).