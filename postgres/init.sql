CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR(20) PRIMARY KEY,
    nickname VARCHAR(20) NOT NULL,
    firstname VARCHAR(40) NOT NULL,
    lastname VARCHAR(40) NOT NULL,
    password VARCHAR(255) NOT NULL,
    plants INT NOT NULL,
    joined DATE
);

CREATE TABLE IF NOT EXISTS plants (
    plant_id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,

    /* Plant Details */
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    age INT, /*years*/
    image_url TEXT, /* Stores the path/link to the image */
    health VARCHAR(50),
    notes TEXT,

    /* Care Needs */
    light_needs varchar(255), /* bright sun, part shade */
    fertilizer_needs VARCHAR(255),

    /* Dates */
    date_acquired DATE,
    date_last_water DATE,
    date_next_water DATE,
    date_last_pot DATE,
    date_next_pot DATE,

    /* Links this plant to a specific user */
    CONSTRAINT plant_owner
    FOREIGN KEY (username)
    REFERENCES users(username)
);



INSERT INTO users (username, nickname, firstname, lastname, password, plants, joined)
VALUES ('user_test', 'nic_test', 'first_test', 'last_test', 'test_passwd', 0, CURRENT_DATE);

INSERT INTO plants (
    username, plant_id, image_url, date_acquired, date_last_water,
    date_next_water, health, notes, light_needs, fertilizer_needs,
    date_last_pot, date_next_pot, plant_name, scientific_name, age
) VALUES (
    'user_test',
    1,
    'https://my-bucket.s3.amazonaws.com/test.jpg',
    '2025-01-15',
    '2026-06-20',
    '2026-06-27',
    'test health',
    'lajgoiwj jfowfeoijwfe knifh kwfeni hew fi wfjniuewfh wiefnj',
    '3',
    'Monthly liquid fertilizer',
    '2025-01-15',
    '2027-01-15',
    'plant test',
    'scientific test',
    1
);