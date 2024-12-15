CREATE TABLE PerishableGoods (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    expiration_date DATE NOT NULL,
    storage_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE
);
