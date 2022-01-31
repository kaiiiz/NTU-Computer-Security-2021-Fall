const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const FL4G = require('./flag.json');


// initialize database

const db = new sqlite3.Database('/tmp/db.sqlite3');
db.exec(`
-- (re)create users table
DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    ip TEXT
);

-- create the chosen one
INSERT INTO users
    (username, password, ip)
VALUES
    ('kirito', '${FL4G}', '48.76.33.33');
`);


// initialize app

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use('/static', express.static('public'));

app.get('/', (req, res) => {
    console.log(req.ip);
    // res.render('index', { ip: req.ip });
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    // console.log(username, password, req.body, req.ip);

    // if (username.includes("'") || password.includes("'"))
        // return res.send('Hacking attempt detected!');   // SQL injection?

    const query = `SELECT username, password, ip FROM users WHERE username = '${username}'`;
    console.log(query);
    db.get(query, (err, user) => {
        if (res.headersSent) return;

        console.log(err, user, password);
        // console.log(user.password === password, user.ip === req.ip);

        if (!err && user && user.password === password && user.ip === req.ip)
            res.send('welcome');
        else
            res.send('failed');
    });

    // querying time should not longer than 50ms
    res.setTimeout(50, () => res.render('failed'));
});

// free welcome page
app.get('/welcome', (req, res) => res.render('welcome'));

app.listen(8080);