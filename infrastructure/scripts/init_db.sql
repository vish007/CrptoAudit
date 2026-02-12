-- Initial database setup script for SimplyFI POR Platform
-- This file runs automatically when PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set default search path
SET search_path TO public;

-- Create ENUM types
DO $$ BEGIN
    CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'deleted');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE engagement_status AS ENUM ('draft', 'active', 'completed', 'archived', 'cancelled');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE engagement_type AS ENUM ('monthly', 'quarterly', 'annual', 'ad_hoc');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE verification_status AS ENUM ('pending', 'verified', 'failed', 'expired');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE reconciliation_status AS ENUM ('pending', 'in_progress', 'completed', 'failed', 'reviewed');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

-- Create indexes for performance
-- These will be complemented by ORM-generated indexes

-- Log all activity for audit trail
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'audit_log'
    ) THEN
        RAISE NOTICE 'Audit log table will be created by ORM migrations';
    END IF;
END $$;

-- Set default session parameters
ALTER DATABASE por_db SET timezone = 'UTC';
ALTER DATABASE por_db SET log_statement = 'all';

-- Create role for application user if not exists
DO
$$
BEGIN
    CREATE ROLE por_user WITH LOGIN PASSWORD 'por_password';
EXCEPTION WHEN others THEN
    RAISE NOTICE 'por_user role already exists';
END
$$;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE por_db TO por_user;
GRANT USAGE ON SCHEMA public TO por_user;
GRANT CREATE ON SCHEMA public TO por_user;

-- The actual tables will be created by SQLAlchemy migrations
-- This script just sets up the database foundation
