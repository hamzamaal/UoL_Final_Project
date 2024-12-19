-- Use the database `food_connector`
USE food_connector;

ALTER TABLE PerishableGoods ADD COLUMN category_id INT;
ALTER TABLE NonPerishableGoods ADD COLUMN category_id INT;
ALTER TABLE PerishableGoods ADD FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE SET NULL;
ALTER TABLE NonPerishableGoods ADD FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE SET NULL;
