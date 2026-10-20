CREATE TABLE IF NOT EXISTS 'users' (
    'id_account'          VARCHAR(191)          NOT NULL,
    'email'               VARCHAR(191)          NOT NULL,
    'hashed_password'     VARCHAR(191)          NOT NULL,
    'first_name'          VARCHAR(100)          NOT NULL,
    'last_name'           VARCHAR(100)          NOT NULL,
    'admin'               TINYINT(1)            NOT NULL DEFAULT 0,
    'is_active'           TINYINT(1)            NOT NULL DEFAULT 1,
    'failed_login_attempts' SMALLINT(6)         NOT NULL DEFAULT 0,
    'locked_until'        DATETIME              NULL,
    'reset_token'         VARCHAR(255)          NULL,
    'reset_token_expires' DATETIME              NULL,
    'email_verified_at'   DATETIME              NULL,
    'created_at'          DATETIME              NOT NULL DEFAULT CURRENT_TIMESTAMP,
    'updated_at'          DATETIME              NULL ON UPDATE CURRENT_TIMESTAMP,
    'last_login_at'       DATETIME              NULL,
    PRIMARY KEY ('id_account'),
    UNIQUE INDEX 'idx_users_email' ('email')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS 'documents' (
    'id_document'         VARCHAR(191)          NOT NULL,
    'id_account'          VARCHAR(191)          NOT NULL,
    'title'               VARCHAR(255)          NOT NULL,
    'description'         TEXT                  NULL,
    'file_path'           VARCHAR(500)          NOT NULL,
    'content_type'       VARCHAR(100)          NOT NULL,
    'format'              VARCHAR(100)          NOT NULL,
    'file_size'           INT                   NOT NULL,
    'created_at'          DATETIME              NOT NULL DEFAULT CURRENT_TIMESTAMP,
    'subject'             VARCHAR(255)          NOT NULL,
    'sector'              VARCHAR(100)          NOT NULL,
    'sector_year'         SMALLINT(6)           NOT NULL,
    'school_year'         SMALLINT(6)           NOT NULL,
    'session'             SMALLINT(6)           NULL,
    PRIMARY KEY ('id_document'),
    INDEX 'idx_documents_id_account' ('id_account'),
    CONSTRAINT 'fk_documents_user'
        FOREIGN KEY ('id_account')
        REFERENCES 'users' ('id_account')
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS 'user_views' (
    'id'                  INT                   NOT NULL AUTO_INCREMENT,
    'document_id'         VARCHAR(191)          NOT NULL,
    'user_id'             VARCHAR(191)          NOT NULL,
    'viewed_at'           DATETIME              NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ('id'),
    INDEX 'idx_user_views_document' ('document_id'),
    INDEX 'idx_user_views_user' ('user_id'),
    CONSTRAINT 'fk_user_views_document'
        FOREIGN KEY ('document_id')
            REFERENCES 'documents' ('id_document')
            ON DELETE CASCADE,
    CONSTRAINT 'fk_user_views_user'
        FOREIGN KEY ('user_id')
            REFERENCES 'users' ('id_account')
            ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
