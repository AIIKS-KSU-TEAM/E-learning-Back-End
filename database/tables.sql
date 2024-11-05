CREATE TABLE IF NOT EXISTS "accounts_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "password" varchar(128) NOT NULL, 
    "last_login" datetime NULL, 
    "is_superuser" bool NOT NULL, 
    "is_staff" bool NOT NULL, 
    "is_active" bool NOT NULL, 
    "date_joined" datetime NOT NULL, 
    "name" varchar(128) NULL, 
    "email" varchar(128) NOT NULL UNIQUE, 
    "phone" varchar(255) NULL, 
    "email_verified_at" datetime NULL, 
    "phone_verified_at" datetime NULL
);