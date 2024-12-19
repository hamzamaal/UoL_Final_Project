-- Use the database `food_connector`
USE food_connector;

CREATE TABLE Donations (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    beneficiary_id INT NOT NULL,
    donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    donation_type ENUM('Perishable', 'Non-Perishable') NOT NULL,
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE,
    FOREIGN KEY (beneficiary_id) REFERENCES Beneficiaries(beneficiary_id) ON DELETE CASCADE
);
