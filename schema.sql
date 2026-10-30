
USE warrantyvault;

INSERT IGNORE INTO products
(user_id, product_name, brand, serial_number,
 purchase_date, purchase_price, warranty_months)
VALUES
(1, 'Laptop', 'HP', 'HP-WV-001', '2025-01-15', 55000, 24),
(1, 'Smartphone', 'Samsung', 'SAM-WV-002', '2025-02-10', 28000, 12),
(1, 'Wireless Mouse', 'Logitech', 'LOG-WV-003', '2025-03-05', 1200, 12),
(1, 'Keyboard', 'Dell', 'DEL-WV-004', '2025-04-12', 1800, 12),
(1, 'Monitor', 'LG', 'LG-WV-005', '2025-05-20', 12500, 24),
(1, 'Headphones', 'Sony', 'SON-WV-006', '2025-06-18', 3500, 12),
(1, 'Tablet', 'Apple', 'APP-WV-007', '2025-07-22', 42000, 12),
(1, 'Smartwatch', 'Noise', 'NOI-WV-008', '2025-08-14', 2500, 12),
(1, 'Printer', 'Canon', 'CAN-WV-009', '2025-09-03', 8500, 24),
(1, 'Router', 'TP-Link', 'TPL-WV-010', '2025-10-11', 2200, 12),
(1, 'External Hard Drive', 'Seagate', 'SEA-WV-011', '2025-11-06', 4800, 24),
(1, 'SSD', 'Samsung', 'SSD-WV-012', '2025-12-19', 6500, 36),
(1, 'Bluetooth Speaker', 'JBL', 'JBL-WV-013', '2024-01-25', 4200, 12),
(1, 'Webcam', 'Logitech', 'LOG-WV-014', '2024-02-17', 3200, 24),
(1, 'Power Bank', 'Ambrane', 'AMB-WV-015', '2024-03-21', 1500, 12),
(1, 'Gaming Console', 'Sony', 'SON-WV-016', '2024-04-08', 45000, 12),
(1, 'Air Conditioner', 'Voltas', 'VOL-WV-017', '2024-05-14', 38000, 24),
(1, 'Refrigerator', 'Samsung', 'SAM-WV-018', '2024-06-09', 32000, 24),
(1, 'Washing Machine', 'LG', 'LG-WV-019', '2024-07-16', 26000, 24),
(1, 'Microwave Oven', 'IFB', 'IFB-WV-020', '2024-08-23', 11500, 24),
(1, 'Smart TV', 'Sony', 'SON-WV-021', '2024-09-12', 52000, 24),
(1, 'Electric Kettle', 'Philips', 'PHI-WV-022', '2025-01-28', 1800, 12),
(1, 'Hair Dryer', 'Philips', 'PHI-WV-023', '2025-03-17', 2200, 12),
(1, 'UPS', 'APC', 'APC-WV-024', '2025-05-08', 7500, 24),
(1, 'Graphics Tablet', 'Wacom', 'WAC-WV-025', '2025-07-30', 9000, 12);

-- Verify the inserted records
SELECT COUNT(*) AS total_products
FROM products
WHERE user_id = 1;

SELECT product_id, product_name, brand, serial_number,
       purchase_date, purchase_price, warranty_months
FROM products
WHERE user_id = 1
ORDER BY product_id;
