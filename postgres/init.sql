CREATE TABLE IF NOT EXISTS users (
    id SERIAL UNIQUE,
    username VARCHAR(20) PRIMARY KEY,
    nickname VARCHAR(20) NOT NULL,
    firstname VARCHAR(40) NOT NULL,
    lastname VARCHAR(40) NOT NULL,
    password VARCHAR(255) NOT NULL,
    plants INT NOT NULL default 0,
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
