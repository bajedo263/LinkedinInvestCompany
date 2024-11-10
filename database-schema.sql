-- Création des tables principales

-- Table des entreprises
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des offres d'emploi
CREATE TABLE job_offers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    salary_min DECIMAL,
    salary_max DECIMAL,
    location VARCHAR(255),
    contract_type VARCHAR(100),
    domain VARCHAR(255),
    skills TEXT[],
    published_date TIMESTAMP,
    source_url TEXT,
    source_platform VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des clés API
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key_value VARCHAR(64) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Table des domaines d'investissement
CREATE TABLE investment_domains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison offres-domaines
CREATE TABLE job_offer_domains (
    job_offer_id INTEGER REFERENCES job_offers(id),
    domain_id INTEGER REFERENCES investment_domains(id),
    confidence_score DECIMAL,
    PRIMARY KEY (job_offer_id, domain_id)
);

-- Index pour améliorer les performances
CREATE INDEX idx_job_offers_company ON job_offers(company_id);
CREATE INDEX idx_job_offers_domain ON job_offers(domain);
CREATE INDEX idx_api_keys_value ON api_keys(key_value);
