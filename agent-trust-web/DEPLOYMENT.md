# Deployment Guide

This guide covers various deployment options for the Agent Trust Network Web UI.

## Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Production Build

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

The built files will be in the `dist/` directory.

## Deployment Options

### 1. Vercel (Recommended)

Vercel provides the easiest deployment experience with automatic HTTPS, CDN, and previews.

#### Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Deploy via GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and import your repository
3. Vercel will automatically detect the Vite configuration
4. Click "Deploy"

#### Vercel Configuration (Optional)

Create `vercel.json` in the project root:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite"
}
```

### 2. Netlify

Netlify is another excellent option with continuous deployment.

#### Deploy via CLI

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Initialize
netlify init

# Build and deploy
npm run build
netlify deploy --prod --dir=dist
```

#### Deploy via Git Integration

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to [netlify.com](https://netlify.com) and add a new site
3. Connect your repository
4. Configure build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Click "Deploy site"

#### Netlify Configuration (Optional)

Create `netlify.toml` in the project root:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 3. GitHub Pages

Free hosting for static sites.

#### Deploy via gh-pages

```bash
# Install gh-pages
npm i -D gh-pages

# Update package.json scripts
```

Add to `package.json`:

```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

Then deploy:

```bash
npm run deploy
```

#### Manual Deployment

```bash
# Build
npm run build

# Copy to gh-pages branch
git checkout -b gh-pages
git add -f dist
git commit -m "Deploy to GitHub Pages"
git subtree push --prefix dist origin gh-pages
```

Update repository settings:
- Go to Settings > Pages
- Source: Deploy from a branch
- Branch: `gh-pages` / `root`

### 4. Cloudflare Pages

Fast global CDN with automatic HTTPS.

#### Deploy via Wrangler CLI

```bash
# Install Wrangler
npm i -g wrangler

# Login
wrangler login

# Deploy
npm run build
wrangler pages deploy dist
```

#### Deploy via Git Integration

1. Push your code to GitHub
2. Go to [dash.cloudflare.com](https://dash.cloudflare.com) > Pages
3. Create a project > Connect to Git
4. Configure build settings:
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
5. Save and Deploy

### 5. AWS S3 + CloudFront

For enterprise-grade deployment.

#### Deploy to S3

```bash
# Install AWS CLI
npm i -g @aws-cli/cli

# Configure AWS credentials
aws configure

# Build
npm run build

# Sync to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Set bucket policy for public access
aws s3api put-bucket-policy --bucket your-bucket-name --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}'
```

#### Set up CloudFront CDN

```bash
# Create CloudFront distribution
aws cloudfront create-distribution --distribution-config '{
  "CallerReference": "agent-trust-web-'$(date +%s)'",
  "Comment": "Agent Trust Network Web UI",
  "DefaultRootObject": "index.html",
  "Origins": {
    "Items": [
      {
        "Id": "S3-your-bucket-name",
        "DomainName": "your-bucket-name.s3.amazonaws.com",
        "S3OriginConfig": {},
        "ConnectionAttempts": 3,
        "ConnectionTimeout": 10,
        "OriginAccessControlId": ""
      }
    ],
    "Quantity": 1
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-your-bucket-name",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"],
      "CachedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"]
      }
    },
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "MinTTL": 0,
    "Compress": true
  },
  "PriceClass": "PriceClass_100",
  "Enabled": true
}'
```

### 6. Docker

For containerized deployments.

#### Build Docker Image

Create `Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Copy custom nginx config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Build and run:

```bash
# Build image
docker build -t agent-trust-web .

# Run container
docker run -d -p 8080:80 --name trust-network agent-trust-web

# Access at http://localhost:8080
```

#### Deploy to Docker Hub

```bash
# Tag image
docker tag agent-trust-web yourusername/agent-trust-web:latest

# Push to Docker Hub
docker push yourusername/agent-trust-web:latest
```

#### Deploy to Kubernetes

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-trust-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-trust-web
  template:
    metadata:
      labels:
        app: agent-trust-web
    spec:
      containers:
      - name: agent-trust-web
        image: yourusername/agent-trust-web:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: agent-trust-web-service
spec:
  selector:
    app: agent-trust-web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

### 7. Traditional Web Server

#### Nginx

```bash
# Build
npm run build

# Copy to web root
sudo cp -r dist/* /var/www/trust-network/

# Configure Nginx
sudo nano /etc/nginx/sites-available/trust-network
```

Nginx config:

```nginx
server {
    listen 80;
    server_name trust-network.example.com;
    root /var/www/trust-network;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/trust-network /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Apache

Create `.htaccess` in `dist/`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

Copy files:

```bash
sudo cp -r dist/* /var/www/html/trust-network/
```

## Environment Variables

The app currently doesn't require any environment variables. All configuration is done through the UI.

## Performance Optimization

### Build Optimization

The Vite configuration already includes:

- Code splitting
- Tree shaking
- Minification
- Asset optimization

### CDN Configuration

For optimal performance:

1. Enable CDN caching for static assets
2. Set up cache headers:
   - HTML: No cache or short cache (1-5 minutes)
   - JS/CSS: Long cache (1 year) with content hashing
   - Images: Long cache (1 year)

### Monitoring

Consider adding:

- Google Analytics or Plausible for usage tracking
- Sentry for error tracking
- Uptime monitoring (Pingdom, UptimeRobot)

## Troubleshooting

### Build Fails

```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

### Deployed Site Shows Blank Page

1. Check browser console for errors
2. Ensure all files are uploaded
3. Verify SPA routing is configured (redirect all routes to index.html)

### Assets Not Loading

1. Check `base` path in `vite.config.ts` if deploying to a subdirectory
2. Verify file paths in the built `index.html`

### Performance Issues

1. Enable gzip/brotli compression on your server
2. Use a CDN for static assets
3. Enable HTTP/2 or HTTP/3
4. Optimize images (use WebP format)

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **CSP**: Consider adding Content Security Policy headers
3. **X-Frame-Options**: Prevent clickjacking
4. **X-Content-Type-Options**: Prevent MIME sniffing

Example security headers (Nginx):

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## Scaling Considerations

The current implementation runs entirely in the browser. For large-scale deployments:

1. **Backend API**: Move simulation logic to a backend server
2. **Database**: Store network state in a database
3. **WebSocket**: Use WebSockets for real-time updates
4. **Caching**: Implement Redis caching for frequently accessed data
5. **Load Balancing**: Distribute traffic across multiple instances

## Support

For issues or questions:
- Open an issue on GitHub
- Check the main README for usage instructions
- Review the code comments for implementation details
