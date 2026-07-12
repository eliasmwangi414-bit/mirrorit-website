const express = require('express');
const session = require('express-session');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const PORT = 3005;

app.use(session({
    secret: 'mirrorit-super-secret-key-2026',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// ========== DATABASE SETUP ==========
const DB_FILE = path.resolve(__dirname, 'site-content.json');
const defaultContent = {
    hero: null,
    logo: null,
    products: {
        "wooden-framed": null,
        "thin-framed": null,
        "frameless": null,
        "wall-mirrors": null,
        "aluminium-framed": null,
        "smart-mirrors": null,
        "vanity": null,
        "accent": null,
        "custom": null
    },
    services: {
        "custom-fabrication": null,
        "professional-installation": null,
        "design-consultation": null,
        "delivery-logistics": null
    },
    gallery: []
};

if (!fs.existsSync(DB_FILE)) {
    fs.writeFileSync(DB_FILE, JSON.stringify(defaultContent, null, 2));
}

function readDB() {
    const raw = fs.readFileSync(DB_FILE, 'utf8');
    const data = JSON.parse(raw);
    // Merge in any missing keys in case DB was created before a new section was added
    return Object.assign({}, defaultContent, data);
}
function writeDB(data) {
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

// ========== GITHUB AUTO-SYNC ==========
function syncToGitHub() {
    const cwd = __dirname;
    const { execSync } = require('child_process');
    setTimeout(() => {
        try {
            execSync('git add -A', { cwd, stdio: 'pipe' });
            try {
                execSync('git commit -m "Auto-update from Admin Panel"', { cwd, stdio: 'pipe' });
            } catch(e) {
                // Nothing to commit — that's fine
                if (!e.stdout || !e.stdout.toString().includes('nothing to commit')) {
                    console.error('[GIT SYNC] Commit error:', e.message);
                    return;
                }
            }
            execSync('git push origin main', { cwd, stdio: 'pipe' });
            console.log('[GIT SYNC] ✅ Pushed to GitHub successfully');
        } catch(e) {
            console.error('[GIT SYNC] ❌ Error:', e.message);
        }
    }, 500); // small delay so the file write completes first
}

// ========== MULTER SETUP ==========
const uploadDir = path.resolve(__dirname, 'images', 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, uploadDir),
    filename: (req, file, cb) => {
        const suffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, suffix + path.extname(file.originalname));
    }
});
const upload = multer({ storage });

// ========== AUTH MIDDLEWARE ==========
const requireAuth = (req, res, next) => {
    if (req.session && req.session.isAdmin) return next();
    res.redirect('/admin-login');
};

// ========== CONTENT API ==========
app.get('/api/site-content', (req, res) => {
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.set('Pragma', 'no-cache');
    res.json(readDB());
});

// Upload hero image
app.post('/api/upload/hero', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    db.hero = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.hero.path });
});

// Upload logo
app.post('/api/upload/logo', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    db.logo = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.logo.path });
});

// Upload product image
app.post('/api/upload/product/:key', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    if (!db.products.hasOwnProperty(req.params.key)) return res.status(404).json({ error: 'Unknown product' });
    db.products[req.params.key] = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.products[req.params.key].path });
});

// Upload service image
app.post('/api/upload/service/:key', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    if (!db.services.hasOwnProperty(req.params.key)) return res.status(404).json({ error: 'Unknown service' });
    db.services[req.params.key] = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.services[req.params.key].path });
});

// Upload gallery image
app.post('/api/upload/gallery', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const { description, mirrorType } = req.body;
    const db = readDB();
    db.gallery.unshift({
        id: Date.now().toString(),
        path: `images/uploads/${req.file.filename}`,
        description,
        mirrorType,
        uploadedAt: new Date().toISOString()
    });
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});

// Delete gallery image
app.post('/api/delete/gallery/:id', requireAuth, (req, res) => {
    const db = readDB();
    db.gallery = db.gallery.filter(img => img.id !== req.params.id);
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});

// Update gallery image description
app.post('/api/update/gallery-desc/:id', requireAuth, (req, res) => {
    const { description } = req.body;
    const db = readDB();
    const item = db.gallery.find(img => img.id === req.params.id);
    if (!item) return res.status(404).json({ error: 'Item not found' });
    item.description = description || '';
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});

// Remove any section image (hero, logo, product, service)
app.post('/api/remove/hero', requireAuth, (req, res) => {
    const db = readDB();
    db.hero = null;
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});
app.post('/api/remove/logo', requireAuth, (req, res) => {
    const db = readDB();
    db.logo = null;
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});
app.post('/api/remove/:section/:key', requireAuth, (req, res) => {
    const { section, key } = req.params;
    const db = readDB();
    if (section === 'product' && db.products.hasOwnProperty(key)) db.products[key] = null;
    else if (section === 'service' && db.services.hasOwnProperty(key)) db.services[key] = null;
    else return res.status(400).json({ error: 'Invalid section/key' });
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});

// ========== ADMIN ROUTES ==========
app.get('/admin-login', (req, res) => {
    const filePath = path.resolve(__dirname, 'admin', 'login.html');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(500).send('Error: ' + err.message);
        res.setHeader('Content-Type', 'text/html');
        res.send(data);
    });
});

app.post('/admin-login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'admin' && password === 'admin123') {
        req.session.isAdmin = true;
        res.redirect('/admin-dashboard');
    } else {
        res.redirect('/admin-login?error=1');
    }
});

app.get('/admin-logout', (req, res) => {
    req.session.destroy();
    res.redirect('/admin-login');
});

app.get('/admin-dashboard', requireAuth, (req, res) => {
    const filePath = path.resolve(__dirname, 'admin', 'dashboard.html');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(500).send('Error: ' + err.message);
        res.setHeader('Content-Type', 'text/html');
        res.send(data);
    });
});

// ========== STATIC FILES ==========
app.use(express.static(__dirname));

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`Admin portal: http://localhost:${PORT}/admin-login`);
});
