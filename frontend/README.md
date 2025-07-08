# 🧬 Baynext Monorepo

Ce monorepo gère :

- `apps/homepage` → landing page baynext.tech (Next.js App Router + shadcn/ui + newsletter + Resend + PostgreSQL)
- `apps/console` → UI future pour la console SaaS (Nexbay)
- `drizzle/` → schéma & migrations
- `packages/` → composants ou configuration partagés

## 🔧 Setup rapide

```bash
# Cloner le repo
git clone git@github.com:<ton-org>/baynext-monorepo.git
cd baynext-monorepo

# Installer les dépendances
npm install
```

## 📦 Structure

```bash
apps/
  homepage/      # landing page baynext.tech
  console/       # future interface utilisateur Nexbay

packages/
  ui/            # composants partagés shadcn (optionnel)
  config/        # configs tsconfig, tailwind, eslint (optionnel)

drizzle/         # schéma + migrations
.env             # variables d'environnement globales
```

## 🛠️ Variables d'environnement (à placer dans `.env`)

```bash
DATABASE_URL=postgresql://... # fourni par Neon
RESEND_API_KEY=your_resend_key
```

## 🚀 Démarrage

```bash
# Lancer l'app homepage
cd apps/homepage
npm run dev
```

## 🧱 Migrations Drizzle

```bash
# Init drizzle (si pas encore fait)
npx drizzle-kit generate:pg

# Push vers la base Neon
npx drizzle-kit push
```

## 📨 Email (production)
- `contact@baynext.tech` → réception via ImprovMX
- `leo@baynext.tech` → envoi via Zoho SMTP (ou autre SMTP provider)

## 🧪 Déploiement Vercel
- Ajouter les apps `homepage` et `console`
- Définir les variables d’environnement dans les paramètres du projet Vercel

---

✨ Construis, déploie et scale ton outil marketing analytique avec Baynext.
