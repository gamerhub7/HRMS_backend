# Supabase PostgreSQL Setup Guide

Complete step-by-step guide to set up Supabase PostgreSQL for HRMS Lite backend.

---

## 📋 Overview

Supabase is an open-source Firebase alternative that provides a PostgreSQL database with a generous free tier. This guide will walk you through setting up Supabase for your HRMS Lite application.

---

## 🚀 Step-by-Step Setup

### Step 1: Create Supabase Account

1. **Go to Supabase**
   - Visit [https://supabase.com](https://supabase.com)

2. **Sign Up**
   - Click "Start your project" or "Sign Up"
   - Choose your registration method:
     - Sign up with GitHub (recommended)
     - Sign up with email

3. **Verify Email** (if using email signup)
   - Check your inbox
   - Click the verification link

---

### Step 2: Create a New Project

1. **Create Organization** (if first time)
   - Click "New organization"
   - Enter organization name
   - Choose free plan
   - Click "Create organization"

2. **Create Project**
   - Click "New project"
   - Fill in project details:
     - **Name**: `hrms-lite` or your preferred name
     - **Database Password**: Generate a strong password
       - **IMPORTANT**: Copy and save this password immediately!
       - You'll need it for the connection string
     - **Region**: Choose closest to you
       - e.g., `Southeast Asia (Singapore)` for Asia
       - e.g., `East US (North Virginia)` for US
     - **Pricing Plan**: Free (default)

3. **Create Project**
   - Click "Create new project"
   - Wait 2-3 minutes for project to be provisioned
   - You'll see "Setting up project..." message

---

### Step 3: Get Database Connection String

1. **Navigate to Database Settings**
   - Click on **Settings** (gear icon) in left sidebar
   - Click on **Database** under "Configuration"

2. **Find Connection String**
   - Scroll down to "Connection string" section
   - You'll see multiple connection formats
   - Click on **"URI"** tab

3. **Copy Connection String**
   - You'll see something like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
   - Click "Copy" button

4. **Replace Password**
   - Replace `[YOUR-PASSWORD]` with your actual database password
   - Example:
   ```
   postgresql://postgres:YourSecurePassword123@db.abc123.supabase.co:5432/postgres
   ```

---

### Step 4: Configure Your Backend

1. **Update `.env` File**
   
   Open `backend/.env` and update:
   
   ```env
   DATABASE_URL=postgresql://postgres:YourPassword@db.abc123.supabase.co:5432/postgres
   CORS_ORIGINS=http://localhost:5173
   ```

2. **Important Notes**:
   - Keep the password secure
   - No spaces in the connection string
   - The database name is typically `postgres` (default)

---

### Step 5: Initialize Database and Test

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start Backend**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Check Initialization**
   - Terminal should show: `Database initialized successfully`
   - This creates the `employees` and `attendance` tables

4. **Test API**
   - Visit `http://localhost:8000/docs`
   - Try creating an employee
   - Data should persist in Supabase

---

### Step 6: Verify in Supabase Dashboard

1. **Open Table Editor**
   - Go to Supabase Dashboard
   - Click **Table Editor** in left sidebar

2. **View Tables**
   - You should see:
     - `employees` table
     - `attendance` table

3. **Check Data**
   - Click on `employees` table
   - You should see any employees you created
   - Click on `attendance` table to see attendance records

---

## 🎯 Database Schema

The application automatically creates these tables:

### `employees` Table
```sql
CREATE TABLE employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### `attendance` Table
```sql
CREATE TABLE attendance (
    id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('Present', 'Absent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🔍 Exploring Your Database

### Using Table Editor

1. **View Data**
   - Click **Table Editor**
   - Select a table
   - View all rows in spreadsheet format

2. **Add/Edit Data**
   - Click "Insert row" to manually add data
   - Click on any cell to edit
   - Click "Save" to commit changes

3. **Filter & Search**
   - Use filters to find specific records
   - Sort by any column

### Using SQL Editor

1. **Open SQL Editor**
   - Click **SQL Editor** in left sidebar
   - Click "New query"

2. **Run SQL Queries**
   ```sql
   -- View all employees
   SELECT * FROM employees;
   
   -- View all attendance records
   SELECT * FROM attendance;
   
   -- Count employees by department
   SELECT department, COUNT(*) as count 
   FROM employees 
   GROUP BY department;
   
   -- Get attendance for specific date
   SELECT e.full_name, a.date, a.status
   FROM attendance a
   JOIN employees e ON a.employee_id = e.employee_id
   WHERE a.date = '2024-01-21';
   ```

3. **Save Queries**
   - Click "Save" to save frequently used queries
   - Name them for easy access later

---

## 🔒 Security Configuration

### Database Access

By default, Supabase allows connections from anywhere. For production:

1. **Enable SSL** (already enabled by default)
2. **Use Environment Variables** for connection strings
3. **Never commit `.env` to Git**

### Row Level Security (Optional)

For additional security, you can enable RLS:

1. Go to **Authentication** → **Policies**
2. Enable RLS for each table
3. Create policies for access control

**Note**: For this assignment, RLS is optional as there's no user authentication.

---

## 📊 Free Tier Limits

Supabase Free Tier includes:
- **Database Size**: 500 MB
- **Bandwidth**: 5 GB/month
- **Monthly Active Users**: Unlimited
- **API Requests**: Unlimited
- **Auto-pause**: Projects pause after 1 week of inactivity

**Perfect for**: Development, testing, small production apps

---

## 🚀 For Deployment

### Environment Variables (Render/Railway/Heroku)

When deploying your backend:

1. **Add Environment Variable**
   - In your hosting platform
   - Add `DATABASE_URL`
   - Use the full Supabase connection string

2. **Example on Render**
   ```
   DATABASE_URL=postgresql://postgres:password@db.abc123.supabase.co:5432/postgres
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

3. **Connection Pooling** (for production)
   - Supabase provides connection pooling
   - Use the pooler connection string for better performance
   - Format: Replace port `5432` with `6543`
   ```
   postgresql://postgres:password@db.abc123.supabase.co:6543/postgres
   ```

---

## 🛠️ Common Issues & Solutions

### Issue 1: "Connection Timeout"
**Solution**:
- Check internet connection
- Verify connection string is correct
- Ensure Supabase project is not paused

### Issue 2: "Password Authentication Failed"
**Solution**:
- Double-check password in connection string
- Reset password in Supabase Dashboard → Settings → Database
- Update `.env` file with new password

### Issue 3: "Database does not exist"
**Solution**:
- Ensure you're using `postgres` as database name
- Don't change the database name in connection string

### Issue 4: "Tables not created"
**Solution**:
- Check if backend initialization ran successfully
- Look for "Database initialized successfully" in terminal
- Manually check Table Editor in Supabase Dashboard

### Issue 5: "SSL Required"
**Solution**:
- Add `?sslmode=require` to connection string
- Example: `postgresql://...@db.xxx.supabase.co:5432/postgres?sslmode=require`

---

## 📈 Monitoring & Analytics

### Database Performance

1. **Navigate to Reports**
   - Click **Reports** in left sidebar
   - View:
     - Database size usage
     - API requests per day
     - Active connections

2. **Database Health**
   - Monitor query performance
   - Check slow queries
   - Review connection stats

### Logs

1. **View Logs**
   - Click **Logs** in left sidebar
   - See all database queries
   - Filter by type (SELECT, INSERT, UPDATE, DELETE)
   - Debug issues with real-time logging

---

## 🔄 Database Backups

Supabase automatically backs up your database:
- **Daily backups** retained for 7 days (Free tier)
- Access via **Database** → **Backups**
- Can restore from any backup point

---

## 💡 Helpful Tips

### 1. Connection Pooling
For production, use connection pooler (port 6543):
```
postgresql://postgres:password@db.xxx.supabase.co:6543/postgres
```

### 2. Direct Connection
For local development, use direct connection (port 5432):
```
postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

### 3. Project Pause
Free tier projects pause after 1 week of inactivity. To wake:
- Visit Supabase dashboard
- Click "Restore project"
- Wait ~30 seconds for reactivation

### 4. Database Migrations
For schema changes:
- Use SQL Editor to run migration scripts
- Or use SQLAlchemy migrations (alembic)
- Save migration scripts for version control

---

## 📝 Example Environment Variables

### Local Development
```env
DATABASE_URL=postgresql://postgres:YourPassword@db.abc123.supabase.co:5432/postgres
CORS_ORIGINS=http://localhost:5173
```

### Production (Render/Vercel)
```env
DATABASE_URL=postgresql://postgres:YourPassword@db.abc123.supabase.co:6543/postgres
CORS_ORIGINS=https://your-frontend.vercel.app,https://hrms-lite.vercel.app
```

---

## 🎉 You're All Set!

Your Supabase PostgreSQL database is now configured and ready!

**Next Steps**:
1. ✅ Test local connection
2. ✅ Deploy backend to Render/Railway
3. ✅ Update production environment variables
4. ✅ Deploy frontend to Vercel
5. ✅ Test end-to-end

---

## 📞 Need Help?

- **Supabase Documentation**: [https://supabase.com/docs](https://supabase.com/docs)
- **Community Discord**: [https://discord.supabase.com](https://discord.supabase.com)
- **GitHub Discussions**: [https://github.com/supabase/supabase/discussions](https://github.com/supabase/supabase/discussions)

---

## 🔗 Useful Links

- [Supabase Homepage](https://supabase.com)
- [Supabase Database Documentation](https://supabase.com/docs/guides/database)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool)
- [Database Backups](https://supabase.com/docs/guides/platform/backups)

---

## 🆚 Supabase vs MongoDB Atlas

### Advantages of Supabase (PostgreSQL)
✅ Relational data structure (better for this use case)
✅ ACID compliance (strong consistency)
✅ Better for complex queries and joins
✅ Built-in realtime subscriptions
✅ Excellent dashboard and SQL editor
✅ 500MB free storage (vs 512MB MongoDB)
✅ Row Level Security for fine-grained access control

### When to Use Each
- **Supabase**: Structured data, relationships, complex queries
- **MongoDB**: Flexible schema, nested documents, rapid prototyping
