const express = require('express');
const mariadb = require('mariadb');
const app = express();

// MariaDB configuration
const pool = mariadb.createPool({
    host: 'localhost',
    user: 'superbroker',
    password: '@Ritagirma123@',
    database: 'sbdb',
    connectionLimit: 5
});

// Express middleware to parse JSON bodies
app.use(express.json());

// Define routes
app.get('/', (req, res) => {
    res.send('SuperBroker API');
});

// Example endpoint to fetch brokers from the database
app.get('/brokers', async (req, res) => {
    let conn;
    try {
        conn = await pool.getConnection();
        const rows = await conn.query('SELECT * FROM brokers');
        res.json(rows);
    } catch (err) {
        console.error('Error connecting to MariaDB:', err);
        res.status(500).send('Internal Server Error');
    } finally {
        if (conn) conn.release(); // release connection
    }
});

// Example endpoint to add a new broker
app.post('/brokers', async (req, res) => {
    const { ip, name } = req.body;
    let conn;
    try {
        conn = await pool.getConnection();
        await conn.query('INSERT INTO brokers (ip, name) VALUES (?, ?)', [ip, name]);
        res.send('Broker added successfully');
    } catch (err) {
        console.error('Error connecting to MariaDB:', err);
        res.status(500).send('Internal Server Error');
    } finally {
        if (conn) conn.release(); // release connection
    }
});

// Start server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`SuperBroker API listening at http://localhost:${port}`);
});
