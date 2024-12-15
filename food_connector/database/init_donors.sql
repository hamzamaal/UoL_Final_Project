CREATE TABLE Donors (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    street_number VARCHAR(10) NOT NULL,
    street_name VARCHAR(255) NOT NULL,
    town VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    province ENUM('Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape') NOT NULL,
    country VARCHAR(50) DEFAULT 'South Africa',
    organization_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
