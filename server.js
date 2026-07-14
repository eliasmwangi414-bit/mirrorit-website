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
        "custom": null,
        "furniture": null
    },
    whyUs: null,
    services: {
        "custom-fabrication": null,
        "professional-installation": null,
        "design-consultation": null,
        "delivery-logistics": null
    },
    serviceDetails: {
        "custom-fabrication-0": null,
        "custom-fabrication-1": null,
        "custom-fabrication-2": null,
        "professional-installation-0": null,
        "professional-installation-1": null,
        "professional-installation-2": null,
        "design-consultation-0": null,
        "design-consultation-1": null,
        "design-consultation-2": null,
        "delivery-logistics-0": null,
        "delivery-logistics-1": null,
        "delivery-logistics-2": null
    },
    gallery: [],
    blog: [
        {
            id: "blog-1",
            title: "How to Choose the Perfect LED Mirror for Your Bathroom",
            date: "July 10, 2026",
            summary: "Discover the difference between front-lit and backlit mirrors, optimal color temperatures (3000K vs 6000K), and why copper-free glass is essential for preventing edge corrosion in humid Nairobi bathrooms.",
            image: "images/products/kitchen-splashback.jpg",
            content: "When selecting an LED mirror for your bathroom, the most critical factor is the glass quality. Standard copper-backed mirrors often develop black edges when exposed to steam over time. At MIRRORIT, all our bathroom mirrors use premium 5mm and 6mm copper-free silver mirror glass, ensuring pristine, crystal-clear reflections that endure for decades."
        },
        {
            id: "blog-2",
            title: "5 Ways Custom Mirrored Furniture Elevates Modern Interiors",
            date: "June 28, 2026",
            summary: "Mirrored console tables and dressers naturally reflect light, making dark apartment hallways and living rooms feel twice as spacious and luxurious.",
            image: "images/products/led-mirror.jpg",
            content: "Mirrored furniture is one of interior design's best-kept secrets. By reflecting both natural sunlight and architectural lighting, a bespoke mirrored console table transforms tight entryways into grand foyers. Each piece crafted by MIRRORIT is precision-aligned and built on solid hardwood cores for maximum durability."
        },
        {
            id: "blog-3",
            title: "The Art of Custom Mirror Fabrication: From Sheet to Wall",
            date: "June 15, 2026",
            summary: "Take a behind-the-scenes look at our Nairobi workshop where we precision-cut, bevel, and polish custom mirrors to fit uneven walls and architectural alcoves perfectly.",
            image: "images/products/glass-railing.jpg",
            content: "No two walls are completely perfectly flat or level. That is why off-the-shelf mirrors frequently leave unsightly gaps or rattle. Our custom fabrication process begins with exact laser measurements on site, followed by precision edge-polishing and custom mounting directly onto your walls."
        }
    ]
};

if (!fs.existsSync(DB_FILE)) {
    fs.writeFileSync(DB_FILE, JSON.stringify(defaultContent, null, 2));
}

function readDB() {
    const raw = fs.readFileSync(DB_FILE, 'utf8');
    const data = JSON.parse(raw);
    const result = Object.assign({}, defaultContent, data);
    result.products = Object.assign({}, defaultContent.products, data.products || {});
    result.services = Object.assign({}, defaultContent.services, data.services || {});
    result.serviceDetails = Object.assign({}, defaultContent.serviceDetails, data.serviceDetails || {});
    if (!result.blog || !Array.isArray(result.blog) || result.blog.length === 0) result.blog = defaultContent.blog;
    return result;
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

// Upload service detail image
app.post('/api/upload/service-detail/:key', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    if (!db.serviceDetails) db.serviceDetails = {};
    if (!db.serviceDetails.hasOwnProperty(req.params.key)) return res.status(404).json({ error: 'Unknown service detail' });
    db.serviceDetails[req.params.key] = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.serviceDetails[req.params.key].path });
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

// Upload Why Us image
app.post('/api/upload/why-us', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    db.whyUs = { path: `images/uploads/${req.file.filename}`, uploadedAt: new Date().toISOString() };
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: db.whyUs.path });
});

// Remove Why Us image
app.post('/api/remove/why-us', requireAuth, (req, res) => {
    const db = readDB();
    db.whyUs = null;
    writeDB(db);
    syncToGitHub();
    res.json({ success: true });
});

// Blog endpoints
app.post('/api/upload/blog/:id', requireAuth, upload.single('image'), (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file' });
    const db = readDB();
    const post = db.blog.find(b => b.id === req.params.id);
    if (!post) return res.status(404).json({ error: 'Post not found' });
    post.image = `images/uploads/${req.file.filename}`;
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, path: post.image });
});

app.post('/api/blog/create', requireAuth, (req, res) => {
    const { title, summary, date, content, image } = req.body;
    const db = readDB();
    const newPost = {
        id: 'blog-' + Date.now(),
        title: title || 'New Blog Post',
        summary: summary || '',
        date: date || new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }),
        content: content || '',
        image: image || 'images/products/led-mirror.jpg'
    };
    db.blog.unshift(newPost);
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, post: newPost });
});

app.post('/api/blog/update/:id', requireAuth, (req, res) => {
    const { title, summary, date, content, image } = req.body;
    const db = readDB();
    const post = db.blog.find(b => b.id === req.params.id);
    if (!post) return res.status(404).json({ error: 'Post not found' });
    if (title !== undefined) post.title = title;
    if (summary !== undefined) post.summary = summary;
    if (date !== undefined) post.date = date;
    if (content !== undefined) post.content = content;
    if (image !== undefined) post.image = image;
    writeDB(db);
    syncToGitHub();
    res.json({ success: true, post });
});

app.post('/api/blog/delete/:id', requireAuth, (req, res) => {
    const db = readDB();
    db.blog = db.blog.filter(b => b.id !== req.params.id);
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
    else if (section === 'service-detail' && db.serviceDetails && db.serviceDetails.hasOwnProperty(key)) db.serviceDetails[key] = null;
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
